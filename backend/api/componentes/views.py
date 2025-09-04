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
import csv
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from django.http import HttpResponse
import io

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

class PersonalExportCSVAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Obtener todos los registros de personal
            personal = Personal.objects.all()
            serializer = PersonalExportSerializer(personal, many=True)
            
            # Obtener fecha y hora actual en Lima (Perú)
            lima_tz = pytz.timezone('America/Lima')
            fecha_exportacion = timezone.now().astimezone(lima_tz).strftime('%Y%m%d_%H%M%S')
            unique_id = str(uuid.uuid4())[:8]
            
            # Preparar la respuesta
            response = HttpResponse(content_type='text/csv; charset=utf-8')
            filename = f"personal_export_{fecha_exportacion}_{unique_id}.csv"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            response['Access-Control-Expose-Headers'] = 'Content-Disposition'
            
            # Escribir CSV delimitado por palote (|)
            writer = csv.writer(response, delimiter='|')
            
            # Escribir encabezados
            headers = [
                'ID', 'DNI', 'Nombre', 'Apellido', 'N° Contrato', 'Dependencia',
                'Fecha Habilitación Acceso', 'Habilitado Por', 'Email', 'User ID',
                'Celular', 'Email Personal', 'RUC', 'Celular Emergencia', 
                'Contacto Emergencia', 'Dirección', 'Distrito', 'Fecha Fin',
                'Fecha Inicio', 'Fecha Nacimiento', 'N° Hijos', 'Padre/Madre',
                'Salario', 'Sexo', 'Teléfono', 'Anexo', 'Área', 'Cargo',
                'Condición', 'Estado', 'Genérica', 'Grupo Ocupacional',
                'Profesión', 'Nivel', 'Régimen', 'Creado Por', 'Edad'
            ]
            writer.writerow(headers)
            
            # Escribir datos
            for item in serializer.data:
                row = [
                    item.get('id', ''),
                    item.get('dni', ''),
                    item.get('nombre', ''),
                    item.get('apellido', ''),
                    item.get('n_contrato', ''),
                    item.get('dependencia_nombre', ''),
                    item.get('fecha_habilitacion_acceso', ''),
                    item.get('habilitado_por', ''),
                    item.get('email', ''),
                    item.get('user_id', ''),
                    item.get('celular', ''),
                    item.get('email_per', ''),
                    item.get('ruc', ''),
                    item.get('cel_emergencia', ''),
                    item.get('cont_emergencia', ''),
                    item.get('direccion', ''),
                    item.get('distrito', ''),
                    item.get('fecha_fin', ''),
                    item.get('fecha_inicio', ''),
                    item.get('fecha_nac', ''),
                    item.get('n_hijos', ''),
                    item.get('padre_madre', ''),
                    item.get('salario', ''),
                    item.get('sexo', ''),
                    item.get('telefono', ''),
                    item.get('anexo_number', ''),
                    item.get('area_nombre', ''),
                    item.get('cargo_nombre', ''),
                    item.get('condicion_nombre', ''),
                    item.get('estado_nombre', ''),
                    item.get('generica_nombre', ''),
                    item.get('grupoo_cupacional_nombre', ''),
                    item.get('profesion_nombre', ''),
                    item.get('nivel_name', ''),
                    item.get('regimen_nombre', ''),
                    item.get('created_by_username', ''),
                    item.get('edad', '')
                ]
                writer.writerow(row)
            
            return response
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR 
            )

class PersonalExportPDFAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Obtener todos los registros de personal
            personal = Personal.objects.all()
            serializer = PersonalExportSerializer(personal, many=True)
            
            if not serializer.data:
                return Response(
                    {'error': 'No hay datos para exportar'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Obtener fecha y hora actual en Lima (Perú)
            lima_tz = pytz.timezone('America/Lima')
            fecha_exportacion = timezone.now().astimezone(lima_tz).strftime('%Y%m%d_%H%M%S')
            unique_id = str(uuid.uuid4())[:8]
            
            # Crear buffer para el PDF
            buffer = io.BytesIO()
            
            # Crear documento PDF en orientación horizontal (landscape)
            from reportlab.lib.pagesizes import landscape, A4
            from reportlab.lib.units import cm
            doc = SimpleDocTemplate(buffer, pagesize=landscape(A4),
                                  leftMargin=1*cm, rightMargin=1*cm,
                                  topMargin=1*cm, bottomMargin=1*cm)
            elements = []
            
            # Estilos
            styles = getSampleStyleSheet()
            title_style = styles['Heading1']
            title_style.alignment = 1  # Centrado
            title_style.fontSize = 14
            
            # Título
            title = Paragraph("REPORTE DE PERSONAL", title_style)
            elements.append(title)
            
            # Espacio después del título
            elements.append(Paragraph("<br/>", styles['Normal']))
            
            # Información de exportación
            export_info = f"Exportado el: {timezone.now().astimezone(lima_tz).strftime('%d/%m/%Y %H:%M:%S')} (Hora Lima) - Total registros: {len(serializer.data)}"
            info_style = styles['Italic']
            info_style.alignment = 1
            info_style.fontSize = 8
            elements.append(Paragraph(export_info, info_style))
            elements.append(Paragraph("<br/>", styles['Normal']))
            
            # Definir columnas principales con anchos proporcionales
            column_widths = [
                0.8*cm,  # ID
                2.0*cm,  # DNI
                3.0*cm,  # Nombre
                3.0*cm,  # Apellido
                2.5*cm,  # N° Contrato
                3.5*cm,  # Dependencia
                2.5*cm,  # Área
                3.0*cm,  # Cargo
                2.0*cm,  # Email
                2.0*cm,  # Celular
                2.5*cm,  # Fecha Nac.
                1.5*cm,  # Edad
                2.5*cm,  # Salario
            ]
            
            # Encabezados principales
            headers = [
                'ID', 'DNI', 'NOMBRE', 'APELLIDO', 'N° CONTRATO',
                'DEPENDENCIA', 'ÁREA', 'CARGO', 'EMAIL', 'CELULAR',
                'FECHA NAC.', 'EDAD', 'SALARIO'
            ]
            
            table_data = [headers]
            
            # Llenar datos
            for item in serializer.data:
                row = [
                    str(item.get('id', '')),
                    str(item.get('dni', '')),
                    str(item.get('nombre', ''))[:20],
                    str(item.get('apellido', ''))[:20],
                    str(item.get('n_contrato', '')),
                    str(item.get('dependencia_nombre', ''))[:25],
                    str(item.get('area_nombre', ''))[:20],
                    str(item.get('cargo_nombre', ''))[:20],
                    str(item.get('email', ''))[:15],
                    str(item.get('celular', '')),
                    str(item.get('fecha_nac', ''))[:10] if item.get('fecha_nac') else '',
                    str(item.get('edad', '')),
                    f"S/. {format(float(item.get('salario', 0)), '.2f')}" if item.get('salario') else 'S/. 0.00'
                ]
                table_data.append(row)
            
            # Crear tabla
            table = Table(table_data, colWidths=column_widths, repeatRows=1)
            
            # Estilo de la tabla
            table_style = TableStyle([
                # Encabezados
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 7),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                ('TOPPADDING', (0, 0), (-1, 0), 6),
                
                # Datos
                ('FONTSIZE', (0, 1), (-1, -1), 6),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (0, 0), (0, -1), 'CENTER'),  # ID centrado
                ('ALIGN', (1, 1), (1, -1), 'CENTER'),  # DNI centrado
                ('ALIGN', (-1, 1), (-1, -1), 'RIGHT'),  # Salario derecha
                ('ALIGN', (-2, 1), (-2, -1), 'CENTER'),  # Edad centrado
                ('LEFTPADDING', (0, 0), (-1, -1), 3),
                ('RIGHTPADDING', (0, 0), (-1, -1), 3),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dcdde1'))
            ])
            
            # Alternar colores de fila para mejor lectura
            for i in range(1, len(table_data)):
                if i % 2 == 0:
                    table_style.add('BACKGROUND', (0, i), (-1, i), colors.HexColor('#f5f6fa'))
                else:
                    table_style.add('BACKGROUND', (0, i), (-1, i), colors.HexColor('#ffffff'))
            
            # Ajustar altura de filas
            for i in range(len(table_data)):
                table_style.add('FONTSIZE', (0, i), (-1, i), 6)
                table_style.add('LEADING', (0, i), (-1, i), 8)
            
            table.setStyle(table_style)
            
            # Añadir la tabla al documento
            elements.append(table)
            
            # Pie de página con información adicional
            elements.append(Paragraph("<br/>", styles['Normal']))
            footer_style = styles['Normal']
            footer_style.fontSize = 7
            footer_style.alignment = 2  # Derecha
            
            footer = Paragraph(f"Página 1 de 1 | Generado por Sistema DGOS", footer_style)
            elements.append(footer)
            
            # Construir PDF
            doc.build(elements)
            
            # Preparar respuesta
            buffer.seek(0)
            response = HttpResponse(buffer, content_type='application/pdf')
            filename = f"personal_export_{fecha_exportacion}_{unique_id}.pdf"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            response['Access-Control-Expose-Headers'] = 'Content-Disposition'
            
            return response
            
        except Exception as e:
            import traceback
            print(f"Error generating PDF: {str(e)}")
            print(traceback.format_exc())
            return Response(
                {'error': f'Error al generar el PDF: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR 
            )