from django.apps import AppConfig

class ApiItemsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ardoise'

    def ready(self):
        # Ceci importera vos signaux pour qu'ils soient connectés
        from . import ardoise_signals
