from __future__ import absolute_import, unicode_literals

# Assurez-vous d'importer l'application Celery de manière correcte.
from .celery import app as celery_app

# Cela garantira que l'application est toujours importée lorsque Django démarre.
__all__ = ('celery_app',)
