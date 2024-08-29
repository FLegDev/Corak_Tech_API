from django.apps import AppConfig

class ApiItemsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'API_ITEMS'

    def ready(self):
        # Ceci importera vos signaux pour qu'ils soient connectés
        from . import API_ITEMS_signals
        # Importer les tâches pour s'assurer qu'elles sont enregistrées
        from . import tasks
