from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Modulo, User

@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ('codename', 'description', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('codename', 'description')

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'show_modulos')
    filter_horizontal = ('modulos', 'groups', 'user_permissions')  # Añade modulos aquí
    
    # Define los fieldsets para incluir el campo modulos
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name', 'email', 'image', 'genero', 'dni', 'celular', 'departamento', 'distrito')}),
        ('Permisos', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'modulos'),  # Añade modulos aquí
        }),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    def show_modulos(self, obj):
        return ", ".join([m.codename for m in obj.modulos.all()])
    show_modulos.short_description = 'Módulos asignados'