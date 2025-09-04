# serializers.py
from rest_framework import serializers
from api.dgos.administracion.models import Personal

class PersonalExportSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', default='-')
    habilitado_por = serializers.CharField(source='habilitado_por.username', default='-')
    edad = serializers.SerializerMethodField()
    dependencia_nombre = serializers.CharField(
        source="dependencia.nombre", read_only=True
    )
    area_nombre = serializers.CharField(source="area.nombre", read_only=True)
    anexo_number = serializers.CharField(source="anexo.number", read_only=True)
    condicion_nombre = serializers.CharField(source="condicion.nombre", read_only=True)
    nivel_name = serializers.CharField(source="nivel.name", read_only=True)
    profesion_nombre = serializers.CharField(source="profesion.nombre", read_only=True)
    cargo_nombre = serializers.CharField(source="cargo.nombre", read_only=True)
    regimen_nombre = serializers.CharField(source="regimen.nombre", read_only=True)
    grupoo_cupacional_nombre = serializers.CharField(
        source="grupo_ocupacional.nombre", read_only=True
    )
    estado_nombre = serializers.CharField(source="estado.nombre", read_only=True)
    generica_nombre = serializers.CharField(source="generica.nombre", read_only=True)

    class Meta:
        model = Personal
        fields = [
            'id', 'dni', 'nombre', 'apellido', 'n_contrato', 'dependencia_nombre',
            'fecha_habilitacion_acceso',
            'habilitado_por', 'email', 'user_id', 'celular', 'email_per', 'ruc',
            'cel_emergencia', 'cont_emergencia', 'direccion', 'distrito',
            'fecha_fin', 'fecha_inicio', 'fecha_nac', 'n_hijos', 'padre_madre',
            'salario', 'sexo', 'telefono', 'anexo_number', 'area_nombre', 'cargo_nombre',
            'condicion_nombre', 'estado_nombre', 'generica_nombre', 'grupoo_cupacional_nombre',
            'profesion_nombre', 'nivel_name', 'regimen_nombre', 'created_by_username', 'edad'
        ]

    def get_edad(self, obj):
        if obj.fecha_nac:
            from datetime import date
            today = date.today()
            return today.year - obj.fecha_nac.year - ((today.month, today.day) < (obj.fecha_nac.month, obj.fecha_nac.day))
        return None

