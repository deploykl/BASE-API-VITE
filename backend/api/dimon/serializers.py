from .models import *
from rest_framework import serializers

class FuentesSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    class Meta:
        model = Fuentes
        fields = '__all__'

class TableroSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    created_by_id = serializers.IntegerField(source='created_by.id', read_only=True)
    fuentes_info = FuentesSerializer(source='fuentes', many=True, read_only=True)  # Para mostrar info detallada
    fuentes = serializers.PrimaryKeyRelatedField(  # Para crear/actualizar con IDs
        queryset=Fuentes.objects.all(),
        many=True,
        required=False
    )
    
    class Meta:
        model = Tablero
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at')

class TableroSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    created_by_id = serializers.IntegerField(source='created_by.id', read_only=True)
    fuentes_info = FuentesSerializer(source='fuentes', many=True, read_only=True)
    fuentes = serializers.PrimaryKeyRelatedField(
        queryset=Fuentes.objects.all(),
        many=True,
        required=False,
        allow_empty=True  # ← Añade esto
    )
    
    class Meta:
        model = Tablero
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at')

    def create(self, validated_data):
        fuentes_data = validated_data.pop('fuentes', [])
        tablero = Tablero.objects.create(**validated_data)
        tablero.fuentes.set(fuentes_data)  # ← Esto debería funcionar con IDs
        return tablero

    def update(self, instance, validated_data):
        fuentes_data = validated_data.pop('fuentes', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if fuentes_data is not None:
            instance.fuentes.set(fuentes_data)
        
        return instance
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