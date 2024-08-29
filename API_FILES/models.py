from django.db import models
import os
from django.utils import timezone  # Importer `timezone` pour obtenir la date et l'heure actuelles
from custom_user_management.models import Corak_API_userProfile

def upload_to(instance, filename):
    """Change the name of the uploaded file to match the desired format."""
    base, extension = os.path.splitext(filename)
    now = timezone.now()
    new_name = f"File_{now.strftime('%Y%m%d%H%M%S')}{extension}"
    return os.path.join('uploads/API_FILES/', new_name)

class UploadedFile(models.Model):
    store_profile = models.ForeignKey(Corak_API_userProfile, on_delete=models.CASCADE, related_name='uploaded_files', null=True)
    file = models.FileField(upload_to=upload_to)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    received_at = models.DateTimeField(default=timezone.now)

class ParsedData(models.Model):
    ACTION_CHOICES = [
        ('p', 'O'),
        ('s', 'S')
    ]

    STICKER_UPDATE_CHOICES = [
        ('n', 'n'),
        ('o', 'o')
    ]

    MEASURE_UNIT_CHOICES = [
        ('K', 'K'),
        ('L', 'L'),
        ('U', 'Unité')
    ]

    PROMOTION_STATUS_CHOICES = [
        ('O', 'Promotion active'),
        ('N', 'Pas de Promotion')
    ]
    store_profile = models.ForeignKey(Corak_API_userProfile, on_delete=models.CASCADE, related_name='parsed_data', null=True)
    # Fields corresponding to the specifications
    updated_at = models.DateTimeField(auto_now=True)
    action = models.CharField(max_length=1, choices=ACTION_CHOICES)
    sticker_update = models.CharField(max_length=1, choices=STICKER_UPDATE_CHOICES)
    gencod_ean = models.CharField(max_length=13)
    main_label = models.CharField(max_length=30)
    secondary_label = models.CharField(max_length=15, blank=True, null=True)
    measure_unit = models.CharField(max_length=1, choices=MEASURE_UNIT_CHOICES)
    content = models.PositiveIntegerField()
    sale_price = models.DecimalField(max_digits=6, decimal_places=2)
    promotion_status = models.CharField(max_length=1, choices=PROMOTION_STATUS_CHOICES)
    top_best_sale = models.CharField(max_length=4)
    management_data = models.CharField(max_length=6)
    decimal_point = models.CharField(max_length=1, default='n')
    presentation_stock = models.CharField(max_length=5)
    restock_unit = models.CharField(max_length=5)
    ug_article = models.CharField(max_length=6)

    def save(self, *args, **kwargs):
        super(ParsedData, self).save(*args, **kwargs)

    def __str__(self):
        return self.gencod_ean
