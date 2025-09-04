from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator, MaxLengthValidator
from .Choices import MARCA_CHOICES, ESTADO_CHOICES

class Anexo(models.Model):
    number = models.IntegerField(
        unique=True, verbose_name="Número"
    )  # Asegura que el nombre sea único

    class Meta:
        verbose_name = "Anexo"
        verbose_name_plural = "Anexos"
        ordering = ["number"]

    def __str__(self):
        return str(self.number)  # Convertir el número a cadena

class Condition(models.Model):
    nombre = models.CharField(
        max_length=255, unique=True, verbose_name="Nombre"
    )  # Asegura que el nombre sea único

    class Meta:
        verbose_name = "Condition"
        verbose_name_plural = "Conditions"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre
    
class Nivel(models.Model):
    name = models.CharField(
        max_length=255, unique=True, verbose_name="Nombre"
    )  # Asegura que el nombre sea único

    class Meta:
        verbose_name = "Nivel"
        verbose_name_plural = "Nivels"
        ordering = ["name"]

    def __str__(self):
        return self.name

class Dependencia(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, unique=True, null=False, blank=False)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

class Area(models.Model):
    dependencia = models.ForeignKey(
        Dependencia, on_delete=models.CASCADE, related_name="areas"
    )  # Relación uno a muchos
    nombre = models.CharField(max_length=255, verbose_name="Nombre", unique=True)

    class Meta:
        verbose_name = "Area"
        verbose_name_plural = "Areas"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

class Profesion(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Profesión")

    class Meta:
        verbose_name = "Profesion"
        verbose_name_plural = "Profesiones"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

class Cargo(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Cargo")

    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

class Regimen(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Cargo")

    class Meta:
        verbose_name = "Regimen"
        verbose_name_plural = "Regimen"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

class GrupoOcupacional(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Grupo Ocupacional")

    class Meta:
        verbose_name = "GrupoOcupacional"
        verbose_name_plural = "GrupoOcupacionales"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Estado(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="nombre")

    class Meta:
        verbose_name = "Estado"
        verbose_name_plural = "Estados"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

class Generica(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="nombre")
    detalle = models.CharField(max_length=255, verbose_name="Detalle")

    class Meta:
        verbose_name = "Generica"
        verbose_name_plural = "Genericas"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Personal(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="personal_profile",
    )
    # Campos para control de acceso
    acceso = models.BooleanField(default=False, verbose_name="acceso al sistema")
    fecha_habilitacion_acceso = models.DateTimeField(
        null=True, blank=True, verbose_name="Fecha de habilitación de acceso"
    )
    habilitado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="personal_habilitado",
        verbose_name="Habilitado por",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="personales_creados",  # <- nombre único
        verbose_name="Creado por",
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Actualizado por",
        related_name="personales_actualizados",  # <- nombre único
    )
    # Datos personales
    dni = models.CharField(max_length=50, unique=True)
    ruc = models.CharField(max_length=50, null=True, blank=True)  # Cambiado a null=True
    nombre = models.CharField(max_length=50, verbose_name="Nombres")
    apellido = models.CharField(max_length=50, verbose_name="Apellidos")
    sexo = models.CharField(
        max_length=1,
        verbose_name="Sexo",
        null=True,
        blank=True,
    )  # AÑADE ESTE CAMPO NUEVO
    fecha_nac = models.DateField(
        verbose_name="Fecha de nacimiento", null=True, blank=True
    )
    distrito = models.CharField(max_length=100, null=True, blank=True)
    direccion = models.CharField(max_length=250, null=True, blank=True)
    cont_emergencia = models.CharField(max_length=250, null=True, blank=True)
    cel_emergencia = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Celuklar de emergencia",
        # validators=[validate_celular],
    )
    padre_madre = models.CharField(max_length=10, null=True, blank=True)
    n_hijos = models.CharField(
        max_length=2,
        null=True,
        blank=True,
    )

    # Información de contacto
    email = models.EmailField(
        unique=True, null=True, blank=True, verbose_name="Correo institucional"
    )
    email_per = models.EmailField(
        unique=True, null=True, blank=True, verbose_name="Correo personal"
    )
    celular = models.CharField(
        max_length=9,
        blank=True,
        null=True,
        validators=[MinLengthValidator(9), MaxLengthValidator(9)],
    )
    telefono = models.CharField(
        max_length=10,  # Aumentado a 10 para incluir código de área
        null=True,
        blank=True,
        verbose_name="Teléfono fijo",
    )
    # Información laboral
    fecha_inicio = models.DateField(verbose_name="Fecha inicio", null=True, blank=True)
    fecha_fin = models.DateField(verbose_name="Fecha fin", null=True, blank=True)
    n_contrato = models.CharField(max_length=50, null=True, blank=True)
    salario = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Salario"
    )
    # Información laboral - RELACIONES AÑADIDAS
    anexo = models.ForeignKey(
        Anexo, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Anexo"
    )
    condicion = models.ForeignKey(
        Condition,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="condición",
    )
    nivel = models.ForeignKey(
        Nivel, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Nivel"
    )
    dependencia = models.ForeignKey(
        Dependencia,
        on_delete=models.SET_NULL,  # Cambiado a SET_NULL para no perder datos
        null=True,
        blank=True,
        related_name="personales",
        verbose_name="Dependencia",
    )
    area = models.ForeignKey(
        Area,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="personales",
        verbose_name="Área",
    )
    profesion = models.ForeignKey(
        Profesion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Profesión",
    )
    cargo = models.ForeignKey(
        Cargo, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Cargo"
    )
    grupo_ocupacional = models.ForeignKey(
        GrupoOcupacional,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Grupo Ocupacional",
    )
    estado = models.ForeignKey(
        Estado,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Estado laboral",
    )
    regimen = models.ForeignKey(
        Regimen,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Regimen",
    )
    generica = models.ForeignKey(
        Generica,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Genérica",
    )

    # Estado y características
    activo = models.BooleanField(default=True)
    es_conductor = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Personal"
        verbose_name_plural = "Personal"
        ordering = ["apellido", "nombre"]

    def __str__(self):
        return f"{self.apellido}, {self.nombre} ({self.dni})"


# Create your models here.
class Vehiculo(models.Model):
    marca = models.CharField(max_length=50, choices=MARCA_CHOICES)
    modelo = models.CharField(max_length=50, null=True, blank=True)
    año = models.PositiveIntegerField()
    placa = models.CharField(max_length=10, unique=True, null=True, blank=True)
    asientos = models.PositiveIntegerField(default=5)  # Máximo 4 personas
    estado = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        choices=ESTADO_CHOICES,
        default="DISPONIBLE",
    )
    kilometraje = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

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
    ipress_departamento = models.CharField(
        max_length=150, null=True, blank=True
    )  # Departamento/Provincia/Distrito
    ipress_provincia = models.CharField(
        max_length=150, null=True, blank=True
    )  # Departamento/Provincia/Distrito
    ipress_distrito = models.CharField(
        max_length=150, null=True, blank=True
    )  # Departamento/Provincia/Distrito
    ipress_disa = models.CharField(
        max_length=150, null=True, blank=True
    )  # Departamento/Provincia/Distrito
    ipress_institucion = models.CharField(
        max_length=150, null=True, blank=True
    )  # Departamento/Provincia/Distrito
    ipress_norte = models.CharField(
        max_length=150, null=True, blank=True
    )  # Departamento/Provincia/Distrito
    ipress_este = models.CharField(
        max_length=150, null=True, blank=True
    )  # Departamento/Provincia/Distrito

    # Personal (máximo 5)
    conductor = models.ForeignKey(
        Personal,
        on_delete=models.PROTECT,
        limit_choices_to={"es_conductor": True, "activo": True},
        related_name="comisiones_conductor",
    )
    participantes = models.ManyToManyField(
        Personal,
        related_name="comisiones_participante",
        limit_choices_to={"activo": True},
        blank=True,
        help_text="Máximo 4 participantes (5 incluyendo conductor)",
    )

    # Control
    reprogramacion = models.BooleanField(default=False)
    motivo_reprogramacion = models.CharField(max_length=50, null=True, blank=True)
    hoja_salida = models.FileField(upload_to="comisiones/hojas/", null=True, blank=True)
    observaciones = models.TextField(blank=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Comisión"
        ordering = ["-fecha_salida"]

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
            raise ValidationError(
                "La fecha de retorno no puede ser anterior a la de salida"
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def lista_personal(self):
        """Devuelve lista estructurada de todo el personal"""
        return [
            {"rol": "Conductor", "persona": self.conductor},
            *[{"rol": "Participante", "persona": p} for p in self.participantes.all()],
        ]
