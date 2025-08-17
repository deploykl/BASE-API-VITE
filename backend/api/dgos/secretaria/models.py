from django.db import models

# Create your models here.
class Vehiculo(models.Model):
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    año = models.PositiveIntegerField()
    placa = models.CharField(max_length=10, unique=True)
    asientos = models.PositiveIntegerField()
    estado = models.CharField(max_length=20, choices=[('disponible', 'Disponible'), ('mantenimiento', 'En mantenimiento'), ('uso', 'En uso')])
    kilometraje = models.PositiveIntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.marca} {self.modelo} - {self.placa}"
    
    