import logging
import os
import json
from celery import shared_task
from django.conf import settings
from django.utils import timezone
from .models import UploadedFile
from API_ITEMS.tasks import process_promo_file
from ardoise.tasks import process_ardoise_file

logger = logging.getLogger('common')

@shared_task
def process_uploaded_file(file_id):
    try:
        # Récupérer l'objet UploadedFile basé sur l'ID
        uploaded_file = UploadedFile.objects.get(id=file_id)
        file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.file.name)

        # Vérifier que le fichier existe
        if not os.path.exists(file_path):
            logger.error(f"Le fichier {file_path} n'existe pas.")
            return

        # Ouvrir et lire le contenu du fichier
        with open(file_path, 'r') as file:
            content = file.read()
            data = json.loads(content)

        # Logique de traitement des données selon le type de fichier
        if uploaded_file.file_type == 'Promo':
            logger.info(f"Déclenchement du traitement du fichier de promotion {file_path}.")
            process_promo_file.delay(data, uploaded_file.store_profile.id)

        elif uploaded_file.file_type == 'Ardoise':
            logger.info(f"Déclenchement du traitement du fichier d'ardoise {file_path}.")
            process_ardoise_file.delay(data, uploaded_file.store_profile.id)

        logger.info(f"Le fichier {uploaded_file.file.name} a été traité avec succès.")

    except Exception as e:
        logger.error(f"Erreur lors du traitement du fichier {file_id}: {e}")
