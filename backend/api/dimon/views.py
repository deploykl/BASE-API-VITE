from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
import pandas as pd
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from django.db.models.functions import ExtractYear, ExtractMonth
from dateutil.parser import parse
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from .models import *
from .serializers import *

User = get_user_model()

class TableroViewSet(viewsets.ModelViewSet):
    queryset = Tablero.objects.all()  # Añade esta línea
    serializer_class = TableroSerializer
    permission_classes = [IsAuthenticated] 
    ordering = ["id"]
    ordering_fields = "__all__"
    filter_backends = (DjangoFilterBackend, OrderingFilter)

# Create your views here.
class LargeResultsSetPagination(PageNumberPagination):
    page_size = 50  # Puedes ajustar este valor
    page_size_query_param = "page_size"
    max_page_size = 200

class ConsultaExternaViewSet(viewsets.ModelViewSet):
    queryset = ConsultaExterna.objects.all()
    serializer_class = ConsultaExternaSerializer
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = LargeResultsSetPagination  # Esto sobrescribe la configuración global

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtro por usuario (para superusuarios que seleccionen un usuario específico)
        user_id = self.request.query_params.get('user_id')
        if user_id and self.request.user.is_superuser:
            queryset = queryset.filter(creado_por__id=user_id)
        elif not self.request.user.is_superuser:
            # Usuarios normales solo ven sus registros
            queryset = queryset.filter(creado_por=self.request.user)
        
        # Resto de tus filtros existentes (mes, año, etc.)
        month = self.request.query_params.get("month")
        year = self.request.query_params.get("year")
        
        if month and year:
            queryset = queryset.filter(
                fecha_hora_cita_otorgada__month=month,
                fecha_hora_cita_otorgada__year=year,
            )
        elif year:
            queryset = queryset.filter(fecha_hora_cita_otorgada__year=year)
        
        return queryset

    @action(detail=False, methods=["post"], url_path="importar-excel")
    def importar_excel(self, request):
        if "file" not in request.FILES:
            return Response(
                {"error": "No se proporcionó archivo"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        file = request.FILES["file"]
        try:
            df = pd.read_excel(file)
            column_mapping = {
                0: "tipo_seguro",
                1: "fecha_nacimiento",
                2: "sexo",
                3: "lugar_procedencia",
                4: "n_hcl",
                5: "fecha_hora_cita_otorgada",
                6: "fecha_hora_atencion",
                7: "diagnostico_medico",
                8: "dx_CIE_10_1",
                9: "dx_CIE_10_2",
                10: "dx_CIE_10_3",
                11: "especialidad",
            }

            if len(df.columns) < len(column_mapping):
                return Response(
                    {
                        "error": f"El archivo Excel debe tener al menos {len(column_mapping)} columnas"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            created_count = 0
            updated_count = 0
            errors = []
            fechas_omitidas = 0
            fecha_limite = datetime(2025, 3, 1).date()

            for index, row in df.iterrows():
                try:
                    data = {}
                    for col_index, field_name in column_mapping.items():
                        if col_index < len(row):
                            data[field_name] = (
                                row[col_index] if not pd.isna(row[col_index]) else None
                            )

                    # Validar campos requeridos
                    required_fields = [
                        "tipo_seguro",
                        "fecha_hora_cita_otorgada",
                        "fecha_hora_atencion",
                    ]
                    missing_fields = [
                        field
                        for field in required_fields
                        if field not in data or data[field] is None
                    ]

                    if missing_fields:
                        errors.append(
                            f"Fila {index + 2}: Faltan campos requeridos: {', '.join(missing_fields)}"
                        )
                        continue

                    # Convertir y validar fechas
                    try:
                        fecha_cita = pd.to_datetime(data["fecha_hora_cita_otorgada"])
                        fecha_atencion = pd.to_datetime(data["fecha_hora_atencion"])

                        # Omitir registros con fechas anteriores
                        if (
                            fecha_cita.date() < fecha_limite
                            or fecha_atencion.date() < fecha_limite
                        ):
                            fechas_omitidas += 1
                            errors.append(
                                f"Fila {index + 2}: Omitida - Fecha cita: {fecha_cita.date()}, "
                                f"Fecha atención: {fecha_atencion.date()}"
                            )
                            continue

                        data["fecha_hora_cita_otorgada"] = fecha_cita
                        data["fecha_hora_atencion"] = fecha_atencion
                    except Exception as e:
                        errors.append(
                            f"Fila {index + 2}: Error en formato de fecha - {str(e)}"
                        )
                        continue

                    # Procesar el resto de campos
                    if "fecha_nacimiento" in data and data["fecha_nacimiento"]:
                        try:
                            data["fecha_nacimiento"] = pd.to_datetime(
                                data["fecha_nacimiento"]
                            ).date()
                        except:
                            data["fecha_nacimiento"] = None

                    if "sexo" in data and data["sexo"]:
                        data["sexo"] = str(data["sexo"]).strip().upper()[:1]

                    for cie_field in ["dx_CIE_10_1", "dx_CIE_10_2", "dx_CIE_10_3"]:
                        if cie_field in data and data[cie_field]:
                            data[cie_field] = str(data[cie_field]).strip()

                    # Crear o actualizar registro
                    consulta, created = ConsultaExterna.objects.update_or_create(
                        fecha_hora_cita_otorgada=data["fecha_hora_cita_otorgada"],
                        defaults={**data, "creado_por": request.user},
                    )

                    if created:
                        created_count += 1
                    else:
                        updated_count += 1

                except Exception as e:
                    errors.append(f"Fila {index + 2}: Error - {str(e)}")
                    continue

            # Mensaje resumen
            message = "Importación completada"
            if fechas_omitidas > 0:
                message = f"Importación completada (omitidas {fechas_omitidas} filas con fechas anteriores a marzo 2025)"

            return Response(
                {
                    "success": True,
                    "message": message,
                    "total_filas": len(df),
                    "creados": created_count,
                    "actualizados": updated_count,
                    "omitidas": fechas_omitidas,
                    "errores": len(errors),
                    "detalle_errores": errors[
                        :20
                    ],  # Mostrar más errores si hay fechas omitidas
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"success": False, "error": f"Error al procesar el archivo: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, methods=["get"], url_path="exportar-todos")
    def exportar_todos(self, request):
        # Filtra solo los registros del usuario actual
        queryset = self.filter_queryset(
            self.get_queryset().filter(creado_por=request.user)
        )

        # Usa values() para optimizar la consulta
        data = queryset.values(
            "tipo_seguro",
            "fecha_nacimiento",
            "sexo",
            "lugar_procedencia",
            "n_hcl",
            "fecha_hora_cita_otorgada",
            "fecha_hora_atencion",
            "diagnostico_medico",
            "dx_CIE_10_1",
            "dx_CIE_10_2",
            "dx_CIE_10_3",
            "especialidad",
            "creado_por__username",
            "fecha_creacion",
        )

        return Response(list(data))

    @action(detail=False, methods=["get"], url_path="meses-disponibles")
    def meses_disponibles(self, request):
        # Obtener los meses/años disponibles en la base de datos
        queryset = self.filter_queryset(self.get_queryset())

        # Si no es superusuario, filtrar por usuario
        if not request.user.is_superuser:
            queryset = queryset.filter(creado_por=request.user)

        meses_data = (
            queryset.annotate(
                year=ExtractYear("fecha_hora_cita_otorgada"),
                month=ExtractMonth("fecha_hora_cita_otorgada"),
            )
            .values("year", "month")
            .distinct()
            .order_by("-year", "-month")
        )

        # Formatear la respuesta
        meses_formateados = [
            {
                "year": item["year"],
                "month": item["month"],
                "label": f"{item['month']}/{item['year']}",
            }
            for item in meses_data
        ]

        return Response(meses_formateados)

    @action(detail=False, methods=["get"], url_path="usuarios-importadores")
    def usuarios_importadores(self, request):
        """Endpoint para obtener usuarios que han importado datos"""
        if not request.user.is_superuser:
            return Response(
                {"detail": "No tiene permiso para ver esta información"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            # Usamos el related_name correcto "consultas_creadas" en lugar de "consultaexterna"
            users = User.objects.filter(
                consultas_creadas__isnull=False
            ).distinct().order_by('username').values('id', 'username')
            
            return Response(list(users))
            
        except Exception as e:
            print(f"Error en usuarios-importadores: {str(e)}")
            return Response(
                {"error": "Error al obtener los usuarios importadores"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )