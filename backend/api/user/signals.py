# api/user/signals.py
from datetime import timezone
from django.contrib.auth import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.core.exceptions import ObjectDoesNotExist
from ipware import get_client_ip
from .models import User, UserAudit

# Señal para actualizar imagen de perfil
@receiver(pre_save, sender=User)
def actualizar_imagen_perfil(sender, instance, **kwargs):
    """
    Actualiza la imagen por defecto cuando cambia el género 
    y el usuario está usando una imagen por defecto.
    """
    if not instance.pk:
        return
    
    try:
        usuario_anterior = User.objects.get(pk=instance.pk)
        
        if usuario_anterior.genero == instance.genero:
            return
        
        imagenes_por_defecto = {
            'img/empty.png',
            'img/hombre.png',
            'img/mujer.png'
        }
        
        if usuario_anterior.image.name in imagenes_por_defecto:
            instance.set_default_image()
            
    except ObjectDoesNotExist:
        pass

