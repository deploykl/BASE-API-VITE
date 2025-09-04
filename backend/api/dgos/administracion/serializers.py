from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from api.user.serializers import ModuloSerializer, UserSerializer
from datetime import date
from .models import *


class AnexoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anexo
        fields = "__all__"


class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = "__all__"


class NivelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nivel
        fields = "__all__"


class DependenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dependencia
        fields = "__all__"


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = "__all__"


class ProfesionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesion
        fields = "__all__"


class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = "__all__"


class RegimenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regimen
        fields = "__all__"


class GrupoOcupacionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrupoOcupacional
        fields = "__all__"


class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = "__all__"


class GenericaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Generica
        fields = "__all__"


class PersonalSerializer(serializers.ModelSerializer):
    anexo_number = serializers.CharField(source="anexo.number", read_only=True)
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

    user = UserSerializer(read_only=True)
    modulos = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()  # ← AÑADE ESTE CAMPO
    edad = serializers.SerializerMethodField()  # ← Nuevo campo para la edad
    created_by_username = serializers.CharField(
        source="created_by.username", read_only=True
    )
    class Meta:
        model = Personal
        fields = "__all__"
    class Meta:
        model = Personal
        fields = "__all__"
        read_only_fields = ["created_by"]
        extra_kwargs = {
            "dni": {
                "required": True,
                "min_length": 8,
                "max_length": 8,
                "error_messages": {
                    "min_length": "El DNI debe tener exactamente 8 dígitos",
                    "max_length": "El DNI debe tener exactamente 8 dígitos",
                    "blank": "El DNI es obligatorio"
                }
            },
            "ruc": {
                "required": True,
                "min_length": 11,
                "max_length": 11,
                "error_messages": {
                    "min_length": "El RUC debe tener exactamente 11 dígitos",
                    "max_length": "El RUC debe tener exactamente 11 dígitos",
                    "blank": "El RUC es obligatorio"
                }
            },
            "celular": {
                "required": False,
                "min_length": 9,
                "max_length": 9,
                "error_messages": {
                    "min_length": "El celular debe tener exactamente 9 dígitos",
                    "max_length": "El celular debe tener exactamente 9 dígitos"
                }
            },
            "telefono": {
                "required": False,
                "min_length": 8,
                "max_length": 8,
                "error_messages": {
                    "min_length": "El teléfono debe tener exactamente 8 dígitos",
                    "max_length": "El teléfono debe tener exactamente 8 dígitos"
                }
            },
            "email": {
                "required": False,
                "allow_blank": True,
                "allow_null": True,
                "error_messages": {"invalid": "Correo inválido"}
            },
            "email_per": {
                "required": False,
                "allow_blank": True,
                "allow_null": True,
                "error_messages": {"invalid": "Correo inválido"}
            },
            "nombre": {"required": True},
            "apellido": {"required": True}
        }
        read_only_fields = ["created_by"]

    def validate_email(self, value):
        """Solo validar unicidad si el email tiene valor"""
        if value in [None, ""]:
            return None
        
        if Personal.objects.filter(email=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError("Este email ya está registrado")
        return value

    def validate_email_per(self, value):
        """Solo validar unicidad si el email_per tiene valor"""
        if value in [None, ""]:
            return None
        
        if Personal.objects.filter(email_per=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError("Este email personal ya está registrado")
        return value
    
    def validate(self, data):
        """Convertir strings vacíos a None"""
        for field in ['email', 'email_per']:
            if field in data and data[field] == "":
                data[field] = None
        return data   
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
    estado_display = serializers.CharField(source="get_estado_display", read_only=True)
    marca_display = serializers.CharField(source="get_marca_display", read_only=True)

    class Meta:
        model = Vehiculo
        fields = "__all__"
        extra_kwargs = {
            "placa": {"required": False, "allow_null": True},
            "modelo": {"required": False, "allow_null": True},
        }


class ComisionSerializer(serializers.ModelSerializer):
    conductor_info = PersonalSerializer(source="conductor", read_only=True)
    vehiculo_info = VehiculoSerializer(source="vehiculo", read_only=True)
    participantes_info = PersonalSerializer(
        source="participantes", many=True, read_only=True
    )
    created_by_username = serializers.CharField(
        source="created_by.username", read_only=True
    )
    conductor_nombre = serializers.CharField(source="conductor.nombre", read_only=True)

    class Meta:
        model = Comision
        fields = "__all__"
        extra_kwargs = {
            "creado_por": {"read_only": True},
            "creado_en": {"read_only": True},
        }
