from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()

@receiver(pre_save, sender=User)
def actualizar_imagen_perfil(sender, instance, **kwargs):
    """
    Actualiza la imagen por defecto cuando cambia el género 
    y el usuario está usando una imagen por defecto.
    """
    # Ignorar usuarios nuevos
    if not instance.pk:
        return
    
    try:
        usuario_anterior = User.objects.get(pk=instance.pk)
        
        # Verificar si el género cambió
        if usuario_anterior.genero == instance.genero:
            return
        
        # Imágenes por defecto a verificar
        imagenes_por_defecto = {
            'img/empty.png',
            'img/hombre.png',
            'img/mujer.png'
        }
        
        # Si estaba usando imagen por defecto, actualizar
        if usuario_anterior.image.name in imagenes_por_defecto:
            instance.set_default_image()
            
    except ObjectDoesNotExist:
        # Caso raro donde el usuario no existe (poco probable)
        pass