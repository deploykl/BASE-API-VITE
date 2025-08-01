from datetime import timezone
from django.db import models, IntegrityError
from django.contrib.auth.models import AbstractUser
from django.core.files.storage import default_storage
from api.Choises import GENDER_CHOICES
import uuid
import os
from django.utils.text import slugify
from api.validators import validate_dni, validate_celular
from django.utils.translation import gettext_lazy as _

from api.gore.models import *


def user_image_path(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    safe_username = slugify(instance.username)
    new_filename = f"{safe_username}-{uuid.uuid4().hex[:8]}{ext}"  # Combina username y parte del UUID
    return f"users/{instance.id}/{new_filename}"

class Modulo(models.Model):
    codename = models.CharField(max_length=50, unique=True)  # Ej: 'admin', 'almacen', 'informatica'
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"({self.codename})"
    
    class Meta:
        verbose_name = "Módulo"
        verbose_name_plural = "Módulos"
        ordering = ['codename']
    
class User(AbstractUser):
    modulos = models.ManyToManyField(Modulo, blank=True, related_name='users')
    image = models.ImageField(upload_to=user_image_path, default="img/empty.png", null=True, blank=True)
    genero = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True, verbose_name="Género")
    dni = models.CharField(max_length=8, null=True, blank=True, verbose_name="DNI", validators=[validate_dni])
    is_online = models.BooleanField(default=False, verbose_name="En línea")
    celular = models.CharField(max_length=9, null=True, blank=True, verbose_name="Celular", validators=[validate_celular])
    distrito = models.CharField(max_length=20, null=True, blank=True, verbose_name="Distrito")
    departamento = models.CharField(max_length=20, null=True, blank=True, verbose_name="Departamento")

    # Campos del establecimiento laboral
    # codigo = models.CharField(max_length=8, null=True, blank=True, verbose_name="Código de establecimiento")
    # institucion = models.CharField(max_length=8, null=True, blank=True, verbose_name="Institución")
    # establecimiento = models.CharField(max_length=200, null=True, blank=True, verbose_name="Nombre del establecimiento")
    # departamento_es = models.CharField(max_length=100, null=True, blank=True, verbose_name="Departamento del establecimiento")
    # provincia_es = models.CharField(max_length=100, null=True, blank=True, verbose_name="Provincia del establecimiento")
    # distrito_es = models.CharField(max_length=100, null=True, blank=True, verbose_name="Distrito del establecimiento")
    # disa = models.CharField(max_length=100, null=True, blank=True, verbose_name="DISA de salud")
    # cod_disa = models.CharField(max_length=20, null=True, blank=True, verbose_name="Código DISA")
    # red = models.CharField(max_length=100, null=True, blank=True, verbose_name="Red de salud")
    # cod_red = models.CharField(max_length=20, null=True, blank=True, verbose_name="Código Red")
    # cod_microred = models.CharField(max_length=20, null=True, blank=True, verbose_name="Código Microred")
    # unidad_ejecutora = models.CharField(max_length=100, null=True, blank=True, verbose_name="Unidad Ejecutora")
    # cod_ue = models.CharField(max_length=20, null=True, blank=True, verbose_name="Código Unidad Ejecutora")
    # categoria = models.CharField(max_length=20, null=True, blank=True, verbose_name="Categoría del establecimiento")
    # direccion = models.CharField(max_length=250, null=True, blank=True, verbose_name="Dirección del establecimiento")
    # norte = models.CharField(max_length=100, null=True, blank=True, verbose_name="Dirección del establecimiento")
    # este = models.CharField(max_length=100, null=True, blank=True, verbose_name="Dirección del establecimiento")

    created_by = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="created_users", verbose_name=_("Creado por"))
    updated_by = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="updated_users", verbose_name=_("Actualizado por"))
    deleted_by = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="deleted_users", verbose_name=_("Eliminado por"))
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Fecha de eliminación"))

    class Meta:
        verbose_name = _("Usuario")
        verbose_name_plural = _("Usuarios")
        ordering = ["-date_joined"]

    def delete(self, deleted_by=None, *args, **kwargs):
        self.deleted_by = deleted_by
        self.deleted_at = timezone.now()
        self.is_active = False
        self.save()

    def save(self, *args, **kwargs):
        """Maneja la imagen por defecto para nuevos usuarios"""
        if not self.pk and not self.image:  # Solo para nuevos usuarios sin imagen
            self.set_default_image()
        super().save(*args, **kwargs)

    def set_default_image(self):
        """Establece la imagen por defecto según el género"""
        if self.genero == "F":
            self.image = "img/mujer.png"
        elif self.genero == "M":
            self.image = "img/hombre.png"
        else:
            self.image = "img/empty.png"

    def delete(self, *args, **kwargs):
        """Elimina la imagen del almacenamiento si no es por defecto"""
        try:
            if self.image and not self.image.name.startswith("img/empty"):
                default_storage.delete(self.image.path)
            super().delete(*args, **kwargs)
        except IntegrityError as e:
            print(f"Error al eliminar usuario: {e}")
            raise


#======================================================= GOBIERNO REGIONAL TEST =======================================
    # Campos de jerarquía
    nivel_acceso = models.CharField(
        max_length=20,
        choices=[
            ('REGIONAL', 'Gobierno Regional'),
            ('RED', 'Red de Salud'),
            ('HOSPITAL', 'Hospital'),
            ('ADMIN', 'Administrador Total')
        ],
        default='HOSPITAL'
    )
    
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, blank=True)
    red = models.ForeignKey(Red, on_delete=models.SET_NULL, null=True, blank=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Métodos para verificar permisos
    def puede_crear_usuario(self, nivel_destino):
        """Determina si puede crear un usuario del nivel especificado"""
        jerarquia = ['HOSPITAL', 'RED', 'REGIONAL', 'ADMIN']
        try:
            return jerarquia.index(self.nivel_acceso) >= jerarquia.index(nivel_destino)
        except ValueError:
            return False
    
    def puede_ver_usuario(self, otro_usuario):
        """Determina si puede ver/modificar a otro usuario"""
        if self.nivel_acceso == 'ADMIN':
            return True
        if self.nivel_acceso == 'REGIONAL':
            return otro_usuario.departamento == self.departamento
        if self.nivel_acceso == 'RED':
            return otro_usuario.red == self.red
        if self.nivel_acceso == 'HOSPITAL':
            return otro_usuario.hospital == self.hospital
        return False
    
    def usuarios_creables(self):
        """Devuelve los niveles de usuario que puede crear"""
        jerarquia = ['HOSPITAL', 'RED', 'REGIONAL']
        try:
            indice = jerarquia.index(self.nivel_acceso)
            return jerarquia[indice+1:] if indice+1 < len(jerarquia) else []
        except ValueError:
            return []