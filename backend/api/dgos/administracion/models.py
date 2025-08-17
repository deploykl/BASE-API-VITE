from django.db import models
from django.conf import settings

from .Choices import MARCA_CHOICES, ESTADO_CHOICES

class Dependencia(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, unique=True, null=False, blank=False)
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
class Personal(models.Model):
    dni = models.CharField(max_length=8,  null=False, blank=False)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    profesion = models.CharField(max_length=50, null=True, blank=True)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.CASCADE, 
        related_name="personales")    
    activo = models.BooleanField(default=True)
    es_conductor = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Personal"
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f"{self.apellido}, {self.nombre} ({self.dni})"

# Create your models here.
class Vehiculo(models.Model):
    marca = models.CharField(max_length=50, choices=MARCA_CHOICES)
    modelo = models.CharField(max_length=50, null=True, blank=True)
    año = models.PositiveIntegerField()
    placa = models.CharField(max_length=10, unique=True, null=True, blank=True)
    asientos = models.PositiveIntegerField(default=5)  # Máximo 4 personas
    estado = models.CharField(max_length=20, null=True, blank=True ,choices=ESTADO_CHOICES, default='DISPONIBLE')
    kilometraje = models.DecimalField(max_digits=10, decimal_places=2 , null=True, blank=True)
    
    def __str__(self):
        return f"{self.marca} {self.modelo} - {self.placa}"
    
class Comision(models.Model):
    # Datos del vehículo
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.PROTECT)
    
    # Datos de la comisión
    tipo = models.CharField(max_length=50)
    motivo = models.TextField()
    fecha_salida = models.DateTimeField(null=True, blank=True)
    fecha_retorno = models.DateTimeField(null=True, blank=True)
    
    # Datos del IPRESS destino
    ipress_codigo = models.CharField(max_length=20, blank=True)
    ipress_nombre = models.CharField(max_length=100, null=True, blank=True)
    ipress_categoria = models.CharField(max_length=50, null=True, blank=True)
    ipress_departamento = models.CharField(max_length=150, null=True, blank=True)  # Departamento/Provincia/Distrito
    ipress_provincia = models.CharField(max_length=150, null=True, blank=True)  # Departamento/Provincia/Distrito
    ipress_distrito = models.CharField(max_length=150, null=True, blank=True)  # Departamento/Provincia/Distrito
    ipress_disa = models.CharField(max_length=150, null=True, blank=True)  # Departamento/Provincia/Distrito
    ipress_institucion = models.CharField(max_length=150, null=True, blank=True)  # Departamento/Provincia/Distrito
    ipress_norte = models.CharField(max_length=150, null=True, blank=True)  # Departamento/Provincia/Distrito
    ipress_este = models.CharField(max_length=150, null=True, blank=True)  # Departamento/Provincia/Distrito
    
    # Personal (máximo 5)
    conductor = models.ForeignKey(
        Personal,
        on_delete=models.PROTECT,
        limit_choices_to={'es_conductor': True, 'activo': True},
        related_name='comisiones_conductor'
    )
    participantes = models.ManyToManyField(
        Personal,
        related_name='comisiones_participante',
        limit_choices_to={'activo': True},
        blank=True,
        help_text="Máximo 4 participantes (5 incluyendo conductor)"
    )
    
    # Control
    reprogramacion = models.BooleanField(default=False)
    motivo_reprogramacion = models.CharField(max_length=50, null=True, blank=True)
    hoja_salida = models.FileField(upload_to='comisiones/hojas/', null=True, blank=True)
    observaciones = models.TextField(blank=True)
    
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    creado_en = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Comisión"
        ordering = ['-fecha_salida']
    
    def __str__(self):
        return f"Comisión #{self.id} - {self.vehiculo.placa}"

    def clean(self):
        from django.core.exceptions import ValidationError
        
        # Validación de capacidad del vehículo (solo si ya existe el objeto)
        if self.pk:  # Solo validar si el objeto ya tiene ID (ya existe en BD)
            total_personas = 1 + self.participantes.count()  # Conductor + participantes
            if total_personas > self.vehiculo.asientos:
                raise ValidationError(
                    f"El vehículo {self.vehiculo.placa} solo tiene capacidad para {self.vehiculo.asientos} personas. "
                    f"Actualmente asignadas: {total_personas}"
                )
        
        # Validación de fechas (siempre se puede hacer)
        if self.fecha_retorno and self.fecha_retorno < self.fecha_salida:
            raise ValidationError("La fecha de retorno no puede ser anterior a la de salida")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def lista_personal(self):
        """Devuelve lista estructurada de todo el personal"""
        return [
            {'rol': 'Conductor', 'persona': self.conductor},
            *[{'rol': 'Participante', 'persona': p} for p in self.participantes.all()]
        ]