from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from api.user.serializers import ModuloSerializer, UserSerializer
from datetime import date
from .models import Dependencia, Personal, Vehiculo, Comision, Area

class DependenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dependencia
        fields = '__all__'

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'
        
class PersonalSerializer(serializers.ModelSerializer):
    dependencia_nombre = serializers.CharField(source='dependencia.nombre', read_only=True)
    area_nombre = serializers.CharField(source='area.nombre', read_only=True)
    anexo_number = serializers.CharField(source='anexo.number', read_only=True)
    condicion_nombre = serializers.CharField(source='condicion.nombre', read_only=True)
    nivel_name = serializers.CharField(source='nivel.name', read_only=True)
    profesion_nombre = serializers.CharField(source='profesion.nombre', read_only=True)
    cargo_nombre = serializers.CharField(source='cargo.nombre', read_only=True)
    regimen_nombre = serializers.CharField(source='regimen.nombre', read_only=True)
    grupoo_cupacional_nombre = serializers.CharField(source='grupo_ocupacional.nombre', read_only=True)
    estado_nombre = serializers.CharField(source='estado.nombre', read_only=True)
    generica_nombre = serializers.CharField(source='generica.nombre', read_only=True)

    user = UserSerializer(read_only=True)
    modulos = serializers.SerializerMethodField() 
    full_name = serializers.SerializerMethodField()  # ← AÑADE ESTE CAMPO
    edad = serializers.SerializerMethodField()  # ← Nuevo campo para la edad
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Personal
        fields = '__all__'
        extra_kwargs = {
            'dni': {'required': True},
            'nombre': {'required': True},
            'apellido': {'required': True}
        }
    read_only_fields = ['created_by']
    @extend_schema_field(str)
    def get_full_name(self, obj) -> str:
        return f"{obj.nombre} {obj.apellido}".strip() or "-"
    
    def get_modulos(self, obj):
        if obj.user:
            return ModuloSerializer(obj.user.modulos.all(), many=True).data
        return []
    
    @extend_schema_field(int)
    def get_edad(self, obj) -> int:
        """Calcula la edad a partir de la fecha de nacimiento"""
        if not obj.fecha_nac:
            return None
        
        today = date.today()
        age = today.year - obj.fecha_nac.year
        
        # Verificar si ya pasó el cumpleaños este año
        if (today.month, today.day) < (obj.fecha_nac.month, obj.fecha_nac.day):
            age -= 1
            
        return age           
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