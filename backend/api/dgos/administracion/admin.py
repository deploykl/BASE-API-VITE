# Register your models here.
from django.contrib import admin
from .models import Dependencia, Personal, Vehiculo, Comision

@admin.register(Dependencia)
class DependenciaAdmin(admin.ModelAdmin):
    list_display = ('nombre','codigo')
    search_fields = ('nombre','codigo')
    ordering = ('codigo',)

@admin.register(Personal)
class PersonalAdmin(admin.ModelAdmin):
    list_display = ('dni', 'apellido', 'nombre', 'dependencia', 'es_conductor', 'activo')
    list_filter = ('dependencia', 'es_conductor', 'activo')
    search_fields = ('dni', 'apellido', 'nombre')
    list_editable = ('activo',)
    ordering = ('apellido', 'nombre')

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'marca', 'modelo', 'año', 'estado', 'kilometraje')
    list_filter = ('marca', 'estado')
    search_fields = ('placa', 'modelo')
    list_editable = ('estado',)

@admin.register(Comision)
class ComisionAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehiculo', 'conductor', 'fecha_salida',)
    search_fields = ('ipress_nombre', 'conductor__nombre', 'conductor__apellido')
    filter_horizontal = ('participantes',)
    date_hierarchy = 'fecha_salida'
    
    fieldsets = (
        ('Datos Principales', {
            'fields': ('vehiculo', 'conductor', 'participantes', 'tipo', 'motivo')
        }),
        ('Fechas', {
            'fields': ('fecha_salida', 'fecha_retorno')
        }),
        ('IPRESS Destino', {
            'fields': (
                'ipress_codigo', 'ipress_nombre', 'ipress_categoria',
                'ipress_departamento', 'ipress_provincia', 'ipress_distrito',
                'ipress_disa', 'ipress_institucion', 'ipress_norte', 'ipress_este'
            )
        }),
        ('Control', {
            'fields': ('reprogramacion', 'motivo_reprogramacion', 'hoja_salida', 'observaciones')
        }),
    )