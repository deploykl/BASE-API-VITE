from .models import *
from rest_framework import serializers


class TableroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tablero
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at')

class ConsultaExternaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultaExterna
        fields = '__all__'
        read_only_fields = ('creado_por', 'fecha_creacion', 'fecha_actualizacion')
        
    def validate(self, data):
        # Validación de campos requeridos
        required_fields = [
            'tipo_seguro', 'fecha_nacimiento', 'sexo', 'lugar_procedencia',
            'n_hcl', 'fecha_hora_cita_otorgada', 'fecha_hora_atencion',
            'diagnostico_medico', 'dx_CIE_10_1', 'especialidad'
        ]
        
        for field in required_fields:
            if field not in data or data[field] in [None, ""]:
                raise serializers.ValidationError({
                    field: "Este campo es obligatorio"
                })
        
        # Validación de fechas
        if data['fecha_hora_atencion'] < data['fecha_hora_cita_otorgada']:
            raise serializers.ValidationError({
                'fecha_hora_atencion': "No puede ser anterior a la fecha de cita"
            })
            
        return data