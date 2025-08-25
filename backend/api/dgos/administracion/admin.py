# Register your models here.
from django.contrib import admin
from .models import Dependencia, Personal, Vehiculo, Comision

@admin.register(Dependencia)
class DependenciaAdmin(admin.ModelAdmin):
    list_display = ('nombre','codigo')
    search_fields = ('nombre','codigo')
    ordering = ('codigo',)

# admin.py
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path
from django.utils.html import format_html
from django.shortcuts import get_object_or_404
from .models import Personal
from api.services.userServices import PersonalAccessService

@admin.register(Personal)
class PersonalAdmin(admin.ModelAdmin):
    list_display = [
        'dni', 'nombre', 'apellido', 'email', 
        'acceso_status', 'acciones_acceso'
    ]
    list_filter = ['acceso', 'activo', 'dependencia']
    search_fields = ['dni', 'nombre', 'apellido', 'email']
    readonly_fields = ['fecha_habilitacion_acceso', 'habilitado_por']
    
    def acceso_status(self, obj):
        """Muestra el estado de acceso con colores"""
        if obj.acceso:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ HABILITADO</span>'
            )
        else:
            return format_html(
                '<span style="color: red; font-weight: bold;">✗ DESHABILITADO</span>'
            )
    acceso_status.short_description = 'Estado Acceso'
    
    def acciones_acceso(self, obj):
        """Botones de acciones de acceso"""
        if obj.acceso:
            return format_html('''
                <button onclick="deshabilitarAcceso({})" class="button" style="background: #dc3545; color: white; border: none; padding: 5px 10px; cursor: pointer;">
                    Deshabilitar
                </button>
                <button onclick="resetearPassword({})" class="button" style="background: #17a2b8; color: white; border: none; padding: 5px 10px; cursor: pointer; margin-left: 5px;">
                    Resetear Password
                </button>
            ''', obj.id, obj.id)
        else:
            return format_html('''
                <button onclick="habilitarAcceso({})" class="button" style="background: #28a745; color: white; border: none; padding: 5px 10px; cursor: pointer;">
                    Habilitar
                </button>
            ''', obj.id)
    acciones_acceso.short_description = 'Acciones'
    
    def get_urls(self):
        """Agrega URLs customizadas al admin"""
        urls = super().get_urls()
        custom_urls = [
            path('<path:object_id>/habilitar-acceso/', self.admin_site.admin_view(self.habilitar_acceso_view)),
            path('<path:object_id>/deshabilitar-acceso/', self.admin_site.admin_view(self.deshabilitar_acceso_view)),
            path('<path:object_id>/resetear-password/', self.admin_site.admin_view(self.resetear_password_view)),
        ]
        return custom_urls + urls
    
    def habilitar_acceso_view(self, request, object_id):
        """View para habilitar acceso desde el admin"""
        personal = get_object_or_404(Personal, id=object_id)
        success, message = PersonalAccessService.habilitar_acceso(personal, request.user)
        
        if success:
            self.message_user(request, message)
        else:
            self.message_user(request, f"Error: {message}", level='error')
        
        return JsonResponse({'success': success, 'message': message})
    
    def deshabilitar_acceso_view(self, request, object_id):
        """View para deshabilitar acceso desde el admin"""
        personal = get_object_or_404(Personal, id=object_id)
        success, message = PersonalAccessService.deshabilitar_acceso(personal, request.user)
        
        if success:
            self.message_user(request, message)
        else:
            self.message_user(request, f"Error: {message}", level='error')
        
        return JsonResponse({'success': success, 'message': message})
    
    def resetear_password_view(self, request, object_id):
        """View para resetear password desde el admin"""
        personal = get_object_or_404(Personal, id=object_id)
        success, message = PersonalAccessService.resetear_password(personal, request.user)
        
        if success:
            self.message_user(request, message)
        else:
            self.message_user(request, f"Error: {message}", level='error')
        
        return JsonResponse({'success': success, 'message': message})
    
    class Media:
        js = ('admin/js/personal_access.js',)

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