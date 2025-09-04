# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
import pandas as pd
from io import BytesIO
from api.dgos.administracion.models import Personal
from .serializers import PersonalExportSerializer

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
            
            # Preparar la respuesta
            output.seek(0)
            response = HttpResponse(
                output.read(),  # read() en lugar de getvalue()
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename="personal.xlsx"'
            response['Content-Length'] = output.tell()
            response['Access-Control-Expose-Headers'] = 'Content-Disposition'
            return response
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )