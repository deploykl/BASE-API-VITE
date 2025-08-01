from .models import *
from rest_framework import serializers
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class ModuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modulo
        fields = ['id', 'name', 'description']
        
class UserSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password', 
            'first_name', 'last_name', 'dni', 'celular',
            'is_active', 'is_staff', 'is_superuser','full_name',
            'date_joined', 'last_login',
            'created_by', 'updated_by'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'date_joined': {'read_only': True},
            'last_login': {'read_only': True},
        }
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or "-"
    
    def validate(self, data):
        # Validación para creación (POST)
        if not self.instance:
            if not data.get('username'):
                raise serializers.ValidationError({"username": "El nombre de usuario es requerido"})
            if not data.get('password'):
                raise serializers.ValidationError({"password": "La contraseña es requerida"})

        # Validaciones para username y email único
        if 'username' in data:
            if User.objects.filter(username=data['username']).exclude(pk=getattr(self.instance, 'pk', None)).exists():
                raise serializers.ValidationError({"username": "Este nombre de usuario ya está en uso"})
    
        if 'email' in data and data['email']:  # Solo validar si email no está vacío
            if User.objects.filter(email=data['email']).exclude(pk=getattr(self.instance, 'pk', None)).exists():
                raise serializers.ValidationError({"email": "Este correo electrónico ya está en uso"})
    
        return data

    def create(self, validated_data):
        # Eliminada la asignación de created_by ya que se manejará en el ViewSet
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        return instance

    def get_created_by(self, obj):
        if obj.created_by:
            return {
                'id': obj.created_by.id,
                'username': obj.created_by.username,
                'full_name': f"{obj.created_by.first_name or ''} {obj.created_by.last_name or ''}".strip()
            }
        return None

    def get_updated_by(self, obj):
        if obj.updated_by:
            return {
                'id': obj.updated_by.id,
                'username': obj.updated_by.username,
                'full_name': f"{obj.updated_by.first_name} {obj.updated_by.last_name}"
            }
        return None
    
class UserProfileSerializer(serializers.ModelSerializer):
    dependencia_name = serializers.ReadOnlyField(source="dependencia.name")
    area_name = serializers.ReadOnlyField(source="area.name")
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            'full_name',
            "dni",
            "celular",
            "image",  # Este es el campo real del modelo
            "dependencia_name",
            "area_name",
        ]
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or "-"
    
    def validate_username(self, value):
        # Verificar si el username ya está en uso por otro usuario
        if User.objects.exclude(pk=self.instance.pk).filter(username=value).exists():
            raise serializers.ValidationError("Este nombre de usuario ya está en uso")
        return value

    def validate_email(self, value):
        # Verificar si el email ya está en uso por otro usuario
        if User.objects.exclude(pk=self.instance.pk).filter(email=value).exists():
            raise serializers.ValidationError("Este correo electrónico ya está en uso")
        return value

    def update(self, instance, validated_data):
        # Manejo especial para la imagen si es necesario
        if "image" in validated_data:
            # Eliminar la imagen anterior si existe
            if instance.image and instance.image.name not in [
                "empty.png",
                "empty-male.png",
                "empty-female.png",
            ]:
                instance.image.delete(save=False)
        return super().update(instance, validated_data)

class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
    confirm_password = serializers.CharField(required=True, min_length=8)

    def validate(self, data):
        # Validar que las contraseñas coincidan
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "Las contraseñas no coinciden"}
            )
        
        # Validar que la nueva contraseña no sea igual a la actual
        if data["new_password"] == data["current_password"]:
            raise serializers.ValidationError(
                {"new_password": "La nueva contraseña no puede ser igual a la actual"}
            )
            
        return data

