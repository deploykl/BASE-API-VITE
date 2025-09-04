from django.contrib import admin
from django.utils.html import format_html
from .models import *

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'description')
    search_fields = ('nombre',)
    
@admin.register(Tablero)
class TableroAdmin(admin.ModelAdmin):
    # Configuración de visualización en la lista
    list_display = ('name', 'formatted_url', 'source', 'last_updated', 'is_active', 'created_by', 'created_at')
    list_filter = ('is_active', 'source', 'created_at')
    search_fields = ('name', 'description', 'source')
    ordering = ('-created_at', 'name')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20
    date_hierarchy = 'created_at'
    
    # Campos a mostrar en el formulario de edición
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'url', 'codigo_embed','description')
        }),
        ('Configuración Técnica', {
            'fields': ('source', 'last_updated', 'update_frequency')
        }),
        ('Estado y Auditoría', {
            'fields': ('is_active', ('created_by', 'created_at'), 'updated_at')
        }),
    )
    
    # Personalización del formulario de creación
    def get_fieldsets(self, request, obj=None):
        if not obj:  # Si es creación
            return (
                ('Información Básica', {
                    'fields': ('name', 'url', 'codigo_embed','description')
                }),
                ('Configuración Técnica', {
                    'fields': ('source', 'last_updated', 'update_frequency')
                }),
            )
        return super().get_fieldsets(request, obj)
    
    # Métodos personalizados para visualización
    def formatted_url(self, obj):
        return format_html('<a href="{}" target="_blank">{}</a>', obj.url, obj.url[:50] + '...' if len(obj.url) > 50 else obj.url)
    formatted_url.short_description = 'URL'
    
    # Auto-selección del usuario creador
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Solo para nuevos objetos
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    # Personalización de acciones
    actions = ['activate_selected', 'deactivate_selected']
    
    def activate_selected(self, request, queryset):
        queryset.update(is_active=True)
    activate_selected.short_description = "Activar tableros seleccionados"
    
    def deactivate_selected(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_selected.short_description = "Desactivar tableros seleccionados"