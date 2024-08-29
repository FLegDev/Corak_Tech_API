# models.py

import os
import json
import logging
from django.db import models
from django.utils import timezone
from django.conf import settings
from custom_user_management.models import Corak_API_userProfile

logger = logging.getLogger('common')

def upload_to(instance, filename):
    base, extension = os.path.splitext(filename)
    now = timezone.now()
    store_profile = instance.store_profile.store_number if instance.store_profile else "unknown"
    new_name = f"{instance.file_type}_{store_profile}_{now.strftime('%Y%m%d%H%M%S')}{extension}"
    subfolder = instance.file_type if instance.file_type else "Unknown"
    return os.path.join('uploads', subfolder, new_name)  # Ne pas ajouter MEDIA_ROOT ici

class UploadedFile(models.Model):
    FILE_TYPE_CHOICES = [
        ('Promo', 'Promotion'),
        ('Ardoise', 'Ardoise')
    ]

    store_profile = models.ForeignKey(Corak_API_userProfile, on_delete=models.CASCADE, related_name='common_uploaded_files', null=True)
    file = models.FileField(upload_to=upload_to, blank=True, null=True)
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        data = kwargs.pop('data', None)
        if not self.file_type:
            self.file_type = self.determine_file_type(data)
        
        super().save(*args, **kwargs)

        # S'assurer que le fichier existe après la sauvegarde du modèle
        if not self.file and data:
            file_type = self.determine_file_type(data)
            file_name = f"{file_type}_{self.store_profile.store_number}_{timezone.now().strftime('%Y%m%d%H%M%S')}.json"
            file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', file_type, file_name)
            logger.debug(f"Creating directory: {os.path.dirname(file_path)}")
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            logger.debug(f"Saving data to file: {file_path}")
            with open(file_path, 'w') as json_file:
                json.dump(data, json_file)
            logger.info(f"Data saved to file: {file_path}")

            # Enregistrer le chemin relatif du fichier dans la base de données
            self.file.name = os.path.relpath(file_path, settings.MEDIA_ROOT)
            super().save(update_fields=['file'])
            logger.info(f"UploadedFile saved with path: {self.file}")

    def determine_file_type(self, data=None):
        try:
            if data:
                content = json.dumps(data)
            else:
                logger.info("Opening file to determine file type.")
                self.file.open('r')
                content = self.file.read().decode('utf-8')
                logger.info("File read successfully.")

            data = json.loads(content)

            # Validate JSON structure and check only the first item
            if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                first_item = data[0] if data else {}

                if 'promotion' in first_item:
                    logger.info("File type determined as Promo.")
                    return 'Promo'
                elif 'certificates' in first_item:
                    logger.info("File type determined as Ardoise.")
                    return 'Ardoise'
                else:
                    logger.info("File type determined as Unknown.")
                    return 'Unknown'
            else:
                logger.error("Invalid JSON structure.")
                return 'Unknown'
        except Exception as e:
            logger.error(f"Error determining file type: {e}")
            return 'Unknown'


    def __str__(self):
        return f"{self.file_type} - {self.store_profile.store_number} - {self.uploaded_at}"
