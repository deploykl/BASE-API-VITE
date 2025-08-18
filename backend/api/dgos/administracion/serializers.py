from rest_framework import serializers
from .models import Dependencia, Personal, Vehiculo, Comision

class DependenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dependencia
        fields = '__all__'

class PersonalSerializer(serializers.ModelSerializer):
    dependencia_nombre = serializers.CharField(source='dependencia.nombre', read_only=True)
    
    class Meta:
        model = Personal
        fields = '__all__'
        extra_kwargs = {
            'dni': {'required': True},
            'nombre': {'required': True},
            'apellido': {'required': True}
        }
        
class VehiculoSerializer(serializers.ModelSerializer):
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    marca_display = serializers.CharField(source='get_marca_display', read_only=True)
    
    class Meta:
        model = Vehiculo
        fields = '__all__'
        extra_kwargs = {
            'placa': {'required': False, 'allow_null': True},
            'modelo': {'required': False, 'allow_null': True}
        }
        
class ComisionSerializer(serializers.ModelSerializer):
    conductor_info = PersonalSerializer(source='conductor', read_only=True)
    vehiculo_info = VehiculoSerializer(source='vehiculo', read_only=True)
    participantes_info = PersonalSerializer(source='participantes', many=True, read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    conductor_nombre = serializers.CharField(source='conductor.nombre', read_only=True)
    
    class Meta:
        model = Comision
        fields = '__all__'
        extra_kwargs = {
            'creado_por': {'read_only': True},
            'creado_en': {'read_only': True}
        }