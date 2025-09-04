# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
import pandas as pd
from io import BytesIO
from api.dgos.administracion.models import Personal
from .serializers import PersonalExportSerializer
from django.utils import timezone
import pytz
import uuid

# views.py (backend mejorado)
# views.py (backend mejorado)
class PersonalExportAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Obtener todos los registros de personal
            personal = Personal.objects.all()
            serializer = PersonalExportSerializer(personal, many=True)
            
            # Convertir a DataFrame de pandas
            df = pd.DataFrame(serializer.data)
            
            # Crear un buffer en memoria
            output = BytesIO()
            
            # Crear el escritor de Excel
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Personal', index=False)
            
            # Obtener fecha y hora actual en Lima (Perú)
            lima_tz = pytz.timezone('America/Lima')
            fecha_exportacion = timezone.now().astimezone(lima_tz).strftime('%Y%m%d_%H%M%S')
            
            # Agregar un identificador único para evitar duplicados
            unique_id = str(uuid.uuid4())[:8]
            
            # Preparar la respuesta
            output.seek(0)
            file_content = output.getvalue()
            output.close()
            
            response = HttpResponse(
                file_content,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            
            # Nombre del archivo con encoding UTF-8
            filename = f"personal_export_{fecha_exportacion}_{unique_id}.xlsx"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            
            # Headers CORS esenciales
            response['Access-Control-Expose-Headers'] = 'Content-Disposition'
            response['Access-Control-Allow-Origin'] = '*'  # O tu dominio específico
            
            return response
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR 
            )