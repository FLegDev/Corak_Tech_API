# zkong_logger.py

import logging
from .models import ZkongLog

class DatabaseLogHandler(logging.Handler):
    def emit(self, record):
        ZkongLog.objects.create(
            level=record.levelname,
            message=record.getMessage()
        )

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(DatabaseLogHandler())


class DatabaseLogHandler(logging.Handler):
    def emit(self, record):
        ZkongLog.objects.create(
            level=record.levelname,
            message=record.getMessage()
        )

        # Déplacer les anciens logs vers le fichier et les supprimer
        old_logs = ZkongLog.objects.all().order_by('-timestamp')[10:]  # Les logs après les 10 plus récents
        for log in old_logs:
            logger.handlers[1].emit(log)  # Utilisez le gestionnaire de fichier pour enregistrer le log
            log.delete()  # Supprimez le log de la base de données


####   Me reste à définir les champs Export2Zkong pour les messages à enregistrer !!!!!!!