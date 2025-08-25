# services.py
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
import re

from api.user.models import Modulo

# Obtener el modelo de usuario personalizado
User = get_user_model()

class PersonalAccessService:
    
    @staticmethod
    def extraer_username_desde_email(email):
        """Extrae el username desde el email (parte antes del @)"""
        if not email or '@' not in email:
            return None
        return email.split('@')[0].lower()
    
    @staticmethod
    def validar_email_para_acceso(email, personal_instance=None):
        """Valida que el email sea adecuado para crear usuario"""
        if not email:
            raise ValidationError("El personal debe tener un email registrado para habilitar acceso")
        
        # Verificar formato básico de email
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValidationError("El formato del email no es válido")
        
        # Verificar que el username no exista
        username = PersonalAccessService.extraer_username_desde_email(email)
        
        # Query para verificar si el username ya existe, excluyendo al usuario actual si existe
        user_query = User.objects.filter(username=username)
        if personal_instance and personal_instance.user:
            user_query = user_query.exclude(id=personal_instance.user.id)
        
        if user_query.exists():
            raise ValidationError(f"El username '{username}' ya existe en el sistema")
        
        return True
    
    
    @staticmethod
    def obtener_modulos_disponibles():
        """Obtiene todos los módulos disponibles"""
        return Modulo.objects.filter(is_active=True)

    @staticmethod
    def habilitar_acceso(personal, habilitado_por, modulos_ids=None, enviar_email=True):
        """Habilita el acceso a un miembro del personal usando su email"""
        try:
            # Validaciones
            if not personal.email:
                return False, "El personal debe tener un email registrado para habilitar acceso"

            PersonalAccessService.validar_email_para_acceso(personal.email, personal)

            if personal.acceso and personal.user:
                return False, "El personal ya tiene acceso habilitado"

            # Extraer username del email
            username = PersonalAccessService.extraer_username_desde_email(personal.email)
            temp_password = get_random_string(12)  # Contraseña temporal

            # Crear o actualizar usuario
            if personal.user:
                user = personal.user
                user.username = username  # Actualizar username si cambió el email
                user.email = personal.email
                user.is_active = True
            else:
                user = User.objects.create_user(
                    username=username,
                    email=personal.email,
                    first_name=personal.nombre,
                    last_name=personal.apellido,
                    password=temp_password,
                    is_active=True
                )
                personal.user = user

            # Asignar módulos si se proporcionaron
            modulos_asignados = []
            if modulos_ids:
                modulos = Modulo.objects.filter(id__in=modulos_ids, is_active=True)
                user.modulos.set(modulos)
                modulos_asignados = list(modulos)  # Guardar para el email

            # Establecer la contraseña temporal
            user.set_password(temp_password)
            user.save()

            # Actualizar campos de control
            personal.acceso = True
            personal.fecha_habilitacion_acceso = timezone.now()
            personal.habilitado_por = habilitado_por
            personal.save()

            # Enviar email con credenciales - CORRECCIÓN AQUÍ
            if enviar_email:
                PersonalAccessService._enviar_credenciales(
                    personal, 
                    username, 
                    temp_password, 
                    modulos_asignados  # Pasar los módulos asignados
                )

            return True, f"Acceso habilitado. Usuario: {username}"

        except ValidationError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Error al habilitar acceso: {str(e)}"

    @staticmethod
    def deshabilitar_acceso(personal, deshabilitado_por):
        """Deshabilita el acceso a un miembro del personal"""
        try:
            if not personal.acceso:
                return False, "El personal no tiene acceso habilitado"
            
            if personal.user:
                # Desactivar el usuario pero no eliminarlo
                personal.user.is_active = False
                personal.user.save()
            
            personal.acceso = False
            personal.fecha_habilitacion_acceso = None
            personal.habilitado_por = None
            personal.save()
            
            return True, "Acceso deshabilitado correctamente"
            
        except Exception as e:
            return False, f"Error al deshabilitar acceso: {str(e)}"
    
    @staticmethod
    def resetear_password(personal, resetado_por, enviar_email=True):
        """Resetea la contraseña de un usuario"""
        try:
            if not personal.acceso or not personal.user:
                return False, "El personal no tiene acceso habilitado"
            
            nueva_password = get_random_string(12)
            personal.user.set_password(nueva_password)
            personal.user.save()
            
            if enviar_email:
                PersonalAccessService._enviar_nueva_password(personal, nueva_password)
            
            return True, "Contraseña reseteada correctamente"
            
        except Exception as e:
            return False, f"Error al resetear contraseña: {str(e)}"
    
    @staticmethod
    def _enviar_credenciales(personal, username, password, modulos_asignados=None):
        """Envía email con credenciales de acceso incluyendo módulos asignados"""
        try:
            subject = 'Credenciales de acceso al sistema'

            # Listar módulos asignados
            modulos_text = ""
            if modulos_asignados:
                modulos_text = "\nMódulos asignados:\n"
                for modulo in modulos_asignados:
                    modulos_text += f"- {modulo.codename}: {modulo.description}\n"

            message = f"""
            Hola {personal.nombre} {personal.apellido},

            Se te ha habilitado acceso al sistema VEXA.

            Tus credenciales son:
            Usuario: {username}
            Contraseña temporal: {password}

            {modulos_text}
            URL del sistema: {getattr(settings, 'FRONTEND_URL', 'http://localhost:8080')}

            Por seguridad, cambia tu contraseña después del primer acceso.

            Saludos,
            Equipo de Sistemas - DGOS
            """

            # DEBUG: Imprimir información para verificar
            print(f"Intentando enviar email a: {personal.email}")
            print(f"Desde: {settings.DEFAULT_FROM_EMAIL}")
            print(f"Servidor SMTP: {settings.EMAIL_HOST}:{settings.EMAIL_PORT}")

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [personal.email],
                fail_silently=False,
            )
            print("Email enviado exitosamente")

        except Exception as e:
            print(f"Error enviando email de credenciales: {e}")
            import traceback
            traceback.print_exc()

    @staticmethod
    def _enviar_nueva_password(personal, nueva_password):
        """Envía email con nueva contraseña"""
        try:
            subject = 'Nueva contraseña de acceso - Sistema VEXA'
            
            message = f"""
            Hola {personal.nombre} {personal.apellido},
            
            Tu contraseña ha sido reseteada.
            
            Tu nueva contraseña es: {nueva_password}
            
            URL del sistema: {getattr(settings, 'FRONTEND_URL', 'http://localhost:8080')}
            
            Por seguridad, cambia tu contraseña después del acceso.
            
            Saludos,
            Equipo de Sistemas - Dirección General de Obras y Saneamiento
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [personal.email],
                fail_silently=False,
            )
            
        except Exception as e:
            print(f"Error enviando email de nueva contraseña: {e}")
            import traceback
            traceback.print_exc()