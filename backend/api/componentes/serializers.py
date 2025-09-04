# serializers.py
from rest_framework import serializers
from api.dgos.administracion.models import Personal

class PersonalExportSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', default='-')
    habilitado_por = serializers.CharField(source='habilitado_por.username', default='-')
    edad = serializers.SerializerMethodField()

    class Meta:
        model = Personal
        fields = [
            'id', 'dni', 'nombre', 'apellido', 'n_contrato', 'dependencia_id',
            'activo', 'es_conductor', 'acceso', 'fecha_habilitacion_acceso',
            'habilitado_por', 'email', 'user_id', 'celular', 'email_per', 'ruc',
            'cel_emergencia', 'cont_emergencia', 'direccion', 'distrito',
            'fecha_fin', 'fecha_inicio', 'fecha_nac', 'n_hijos', 'padre_madre',
            'salario', 'sexo', 'telefono', 'anexo_id', 'area_id', 'cargo_id',
            'condicion_id', 'estado_id', 'generica_id', 'grupo_ocupacional_id',
            'profesion_id', 'nivel_id', 'regimen_id', 'created_by_username', 'edad'
        ]

    def get_edad(self, obj):
        if obj.fecha_nac:
            from datetime import date
            today = date.today()
            return today.year - obj.fecha_nac.year - ((today.month, today.day) < (obj.fecha_nac.month, obj.fecha_nac.day))
        return None
