from django.apps import AppConfig

class CorakEslConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Corak_ESL'

    def ready(self):
        # Importer les signaux ici pour s'assurer qu'ils sont prêts lorsque Django démarre.
        from . import signals  # C'est ici que nous importons le module signals.py
