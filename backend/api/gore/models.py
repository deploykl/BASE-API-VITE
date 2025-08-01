from django.db import models

# Create your models here.
class Departamento(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return self.nombre

class Red(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, unique=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='redes')
    
    def __str__(self):
        return f"{self.nombre} ({self.departamento})"

class Hospital(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, unique=True)
    red = models.ForeignKey(Red, on_delete=models.CASCADE, related_name='hospitales')
    
    def __str__(self):
        return f"{self.nombre} ({self.red})"