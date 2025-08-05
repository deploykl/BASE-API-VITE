from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.files.storage import default_storage
from api.Choises import GENDER_CHOICES
import uuid
import os
from django.utils.text import slugify
from api.validators import validate_dni, validate_celular
from django.utils.translation import gettext_lazy as _

from api.gore.models import *
from simple_history.models import HistoricalRecords


def user_image_path(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    safe_username = slugify(instance.username)
    new_filename = f"{safe_username}-{uuid.uuid4().hex[:8]}{ext}"  # Combina username y parte del UUID
    return f"users/{instance.id}/{new_filename}"


class Modulo(models.Model):
    codename = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"({self.codename})"

    class Meta:
        verbose_name = "Módulo"
        verbose_name_plural = "Módulos"
        ordering = ["codename"]


class User(AbstractUser):
    modulos = models.ManyToManyField(Modulo, blank=True, related_name="users")
    image = models.ImageField(
        upload_to=user_image_path, default="img/empty.png", null=True, blank=True
    )
    genero = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        null=True,
        blank=True,
        verbose_name="Género",
    )
    dni = models.CharField(
        max_length=8,
        null=True,
        blank=True,
        verbose_name="DNI",
        validators=[validate_dni],
    )
    is_online = models.BooleanField(default=False, verbose_name="En línea")
    celular = models.CharField(
        max_length=9,
        null=True,
        blank=True,
        verbose_name="Celular",
        validators=[validate_celular],
    )
    distrito = models.CharField(
        max_length=20, null=True, blank=True, verbose_name="Distrito"
    )
    departamento = models.CharField(
        max_length=20, null=True, blank=True, verbose_name="Departamento"
    )
    history = HistoricalRecords(
        table_name="user_historicaluser",
        inherit=False,
        excluded_fields=["password", "last_login", "is_online"],
    )
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
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación"
    )
    created_by = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_users",
        verbose_name=_("Creado por"),
    )
    updated_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Fecha de actualización"
    )
    updated_by = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_users",
        verbose_name=_("Actualizado por"),
    )
    deactivated_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Fecha de desactivación"
    )
    deactivated_by = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="deactivated_users",
        verbose_name=_("Desactivado por"),
    )
    activated_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Fecha de activación"
    )
    activated_by = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="activated_users",
        verbose_name=_("Activado por"),
    )

    class Meta:
        verbose_name = _("Usuario")
        verbose_name_plural = _("Usuarios")
        ordering = ["-date_joined"]

    class Meta:
        verbose_name = _("Usuario")
        verbose_name_plural = _("Usuarios")
        ordering = ["-date_joined"]

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
        """Elimina físicamente el usuario y su imagen si no es por defecto"""
        request = kwargs.pop("request", None)
        
        # Elimina la imagen si no es por defecto
        try:
            if self.image and not self.image.name.startswith(
                ("img/empty", "img/mujer", "img/hombre")
            ):
                default_storage.delete(self.image.path)
        except Exception as e:
            print(f"Error al eliminar imagen: {e}")
        
        # Eliminación física (llama al delete() original de models.Model)
        super().delete(*args, **kwargs)

