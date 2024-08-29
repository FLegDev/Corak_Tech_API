from django.apps import AppConfig


class CommonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'common'

    def ready(self):
            import common.signals  # Assurez-vous que les signaux sont importés lorsque l'application est prête