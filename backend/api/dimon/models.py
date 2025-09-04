from django.conf import settings
from django.db import models, IntegrityError
from .Choises import GENDER_CHOICES
from django.core.exceptions import ValidationError

class Categoria(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Nombre del Tablero")
    description = models.TextField(blank=True, null=True, verbose_name="Descripción")

    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ["nombre"]
        
class Fuentes(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Nombre del Tablero")
    frecuencia = models.TextField(blank=True, null=True, verbose_name="Descripción")
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Categoria",
    )
    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        verbose_name = "Fuente"
        verbose_name_plural = "Fuentes"
        ordering = ["nombre"]        

# Create your models here.
class Tablero(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nombre del Tablero")
    url = models.URLField(max_length=500, verbose_name="URL del Tablero")
    codigo_embed = models.TextField()
    description = models.TextField(blank=True, null=True, verbose_name="Descripción")
    source = models.CharField(max_length=255, verbose_name="Fuente de datos")
    last_updated = models.DateTimeField(verbose_name="Última actualización")
    update_frequency = models.TextField(
        blank=True, null=True, verbose_name="Frecuencia de actualización"
    )
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de modificación"
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Tablero"
        verbose_name_plural = "Tableros"
        ordering = ["name"]


class ConsultaExterna(models.Model):
    tipo_seguro = models.CharField(max_length=70)
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(max_length=1, choices=GENDER_CHOICES)
    lugar_procedencia = models.CharField(max_length=100)
    n_hcl = models.CharField(max_length=20, verbose_name="Número de Historia Clínica")
    fecha_hora_cita_otorgada = models.DateTimeField()
    fecha_hora_atencion = models.DateTimeField()
    diagnostico_medico = models.TextField()
    dx_CIE_10_1 = models.CharField(
        max_length=10, verbose_name="Diagnóstico CIE-10 Principal"
    )
    dx_CIE_10_2 = models.CharField(
        max_length=10,
        verbose_name="Diagnóstico CIE-10 Secundario",
        blank=True,
        null=True,
    )
    dx_CIE_10_3 = models.CharField(
        max_length=10,
        verbose_name="Diagnóstico CIE-10 Terciario",
        blank=True,
        null=True,
    )
    especialidad = models.CharField(max_length=100)
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="consultas_creadas",
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Consulta {self.id} - {self.fecha_hora_atencion.date()}"

    def clean(self):
        super().clean()
        # Validar campos requeridos
        required_fields = {
            "tipo_seguro": "El tipo de seguro es obligatorio",
            "fecha_nacimiento": "La fecha de nacimiento es obligatoria",
            "sexo": "El sexo es obligatorio",
            "lugar_procedencia": "El lugar de procedencia es obligatorio",
            "n_hcl": "El número de historia clínica es obligatorio",
            "fecha_hora_cita_otorgada": "La fecha/hora de cita otorgada es obligatoria",
            "fecha_hora_atencion": "La fecha/hora de atención es obligatoria",
            "diagnostico_medico": "El diagnóstico médico es obligatorio",
            "dx_CIE_10_1": "El diagnóstico CIE-10 principal es obligatorio",
            "especialidad": "La especialidad es obligatoria",
        }

        for field, error_msg in required_fields.items():
            if not getattr(self, field):
                raise ValidationError({field: error_msg})

        # Validación adicional para fechas
        if self.fecha_hora_cita_otorgada and self.fecha_hora_atencion:
            if self.fecha_hora_atencion < self.fecha_hora_cita_otorgada:
                raise ValidationError(
                    "La fecha de atención no puede ser anterior a la fecha de cita otorgada"
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
