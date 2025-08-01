from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Departamento, Red, Hospital

User = get_user_model()

class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = ['id', 'nombre']

class RedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Red
        fields = ['id', 'nombre']

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['id', 'nombre']
        
class UserGoreSerializer(serializers.ModelSerializer):
    nivel_acceso = serializers.CharField()
    departamento = DepartamentoSerializer(read_only=True)
    red = RedSerializer(read_only=True)
    hospital = HospitalSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'is_active', 'is_staff', 'is_superuser', 'nivel_acceso',
            'departamento', 'red', 'hospital', 'date_joined'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def get_departamento_info(self, obj):
        return {'id': obj.departamento.id, 'nombre': obj.departamento.nombre} if obj.departamento else None
    
    def get_red_info(self, obj):
        return {'id': obj.red.id, 'nombre': obj.red.nombre} if obj.red else None
    
    def get_hospital_info(self, obj):
        return {'id': obj.hospital.id, 'nombre': obj.hospital.nombre} if obj.hospital else None