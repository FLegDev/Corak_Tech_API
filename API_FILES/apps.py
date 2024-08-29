from django.apps import AppConfig


class ApiFilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'API_FILES'
    def ready(self):
        from . import API_FILES_signals

