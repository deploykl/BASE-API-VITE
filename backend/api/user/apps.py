from django.apps import AppConfig

class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.user'

    def ready(self):
        # Importa las señales cuando la app está lista
        import api.user.signals  # noqa