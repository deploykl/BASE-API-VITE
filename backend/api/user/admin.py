from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Modulo
from django.utils.translation import gettext_lazy as _

# Admin para el modelo Modulo
@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ('codename', 'description', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('codename', 'description')
    ordering = ('codename',)
    fieldsets = (
        (None, {
            'fields': ('codename', 'description', 'is_active')
        }),
    )

# Admin personalizado para el modelo User
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'email', 'image', 'genero', 'dni', 'celular' , 'nivel_acceso')
        }),
        (_('Location info'), {
            'fields': ('departamento', 'distrito'),
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'modulos'),
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined')
        }),
        (_('Work info'), {
            'fields': ('is_online',),
        }),
        (_('Audit'), {
            'fields': ('created_by', 'updated_by', 'deleted_by', 'deleted_at'),
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name'),
        }),
    )
    
    list_display = (
        'username', 'email', 'first_name', 'last_name', 
        'genero', 'is_staff', 'is_superuser', 'is_active',
        'modulos_list', 'image_preview'
    )
    
    list_filter = (
        'genero', 'is_staff', 'is_superuser', 'is_active',
        'modulos', 'departamento', 'distrito'
    )
    
    search_fields = ('username', 'first_name', 'last_name', 'email', 'dni', 'celular')
    ordering = ('-date_joined',)
    filter_horizontal = ('groups', 'user_permissions', 'modulos')
    readonly_fields = ('created_by', 'updated_by', 'deleted_by', 'deleted_at', 'last_login', 'date_joined')
    
    def modulos_list(self, obj):
        return ", ".join([m.codename for m in obj.modulos.all()])
    modulos_list.short_description = 'Módulos'
    
    def image_preview(self, obj):
        from django.utils.html import format_html
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "-"
    image_preview.short_description = 'Imagen'
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es un nuevo usuario
            obj.created_by = request.user
        else:  # Si se está actualizando
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)
    
    def delete_model(self, request, obj):
        obj.deleted_by = request.user
        obj.is_active = False
        obj.save()