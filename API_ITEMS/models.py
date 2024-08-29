import logging
from django.db import models
from custom_user_management.models import Corak_API_userProfile
from django.utils import timezone

logger = logging.getLogger(__name__)

class Custom(models.Model):
    store_profile = models.ForeignKey(Corak_API_userProfile, on_delete=models.CASCADE, related_name='custom_items', null=True)
    code_article = models.CharField(max_length=255, null=True)
    ADVCOND_CODE = models.CharField(max_length=255, blank=True, null=True)
    ADVCARACT_MIN = models.IntegerField(blank=True, null=True)
    CSTTOT_KEY = models.CharField(max_length=3, choices=[('REM', '%'), ('RED', '€'), ('PME', 'Avantage carte')], blank=True, null=True)
    ADVTYPE_ID = models.IntegerField(blank=True, null=True)
    BINID = models.CharField(max_length=1, choices=[('0', '0'), ('1', '1')], blank=True, null=True)
    ADV_ID = models.CharField(max_length=255, blank=True, null=True)
    ADV_ACTIVE = models.CharField(max_length=1, choices=[('0', '0'), ('1', '1')], blank=True, null=True)
    DATE_EXTRACT = models.DateTimeField(blank=True, null=True)
    ADV_PROFIL = models.CharField(max_length=255, blank=True, null=True)
    ADVCARACT_AMOUNT = models.IntegerField(blank=True, null=True)
    product = models.OneToOneField('Product', on_delete=models.CASCADE, null=True, blank=True, related_name='custom_product')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('store_profile', 'code_article')

    def __str__(self):
        return self.ADV_ID or ''

    def save(self, *args, **kwargs):
        logger.info(f"Saving Custom: {self.code_article}")
        super().save(*args, **kwargs)
        logger.info(f"Custom saved: {self.code_article}")

class Promotion(models.Model):
    store_profile = models.ForeignKey(Corak_API_userProfile, on_delete=models.CASCADE, related_name='promotion_items', null=True)
    code_article = models.CharField(max_length=255, null=True)
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=False)  # Pour marquer la promotion active/inactive
    product = models.OneToOneField('Product', on_delete=models.CASCADE, null=True, blank=True, related_name='promotion_product')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('store_profile', 'code_article')
    
    def apply_delta(self):
        # La logique pour appliquer le delta est désormais d'utiliser directement le modèle Custom
        if self.product and self.product.custom:
            adv_active = self.product.custom.ADV_ACTIVE
            # Appliquez des actions basées sur adv_active. Par exemple:
            if adv_active == '0':
                self.end = timezone.now()
                self.save()
                logger.info(f"Promotion {self.code_article} désactivée car ADV_ACTIVE est 0.")
            else:
                logger.info(f"Promotion {self.code_article} active.")
    
    def update_status(self):
        now = timezone.now()
        if self.start <= now <= self.end:
            self.is_active = True
        else:
            self.is_active = False
        self.save()
        logger.info(f"Promotion status updated: {self.code_article}, is_active: {self.is_active}")

    def __str__(self):
        return f"{self.start} to {self.end}"

    def save(self, *args, **kwargs):
        logger.info(f"Saving Promotion: {self.code_article}")
        super().save(*args, **kwargs)
        logger.info(f"Promotion saved: {self.code_article}")

class RefreshSchedule(models.Model):
    store_profile = models.ForeignKey(Corak_API_userProfile, on_delete=models.CASCADE, related_name='refresh_schedules_items', null=True)
    code_article = models.CharField(max_length=255, null=True)
    date = models.DateTimeField(null=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True, blank=True, related_name='refresh_schedules_product')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('store_profile', 'code_article')

    def __str__(self):
        return self.date.strftime('%Y-%m-%d %H:%M:%S')

    def save(self, *args, **kwargs):
        logger.info(f"Saving RefreshSchedule: {self.code_article} for date {self.date}")
        super().save(*args, **kwargs)
        logger.info(f"RefreshSchedule saved: {self.code_article} for date {self.date}")

class Product(models.Model):
    store_profile = models.ForeignKey(Corak_API_userProfile, on_delete=models.CASCADE, related_name='product_items', null=True)
    code_article = models.CharField(max_length=255, null=True)
    custom = models.OneToOneField(Custom, on_delete=models.CASCADE, null=True, blank=True, related_name='product_custom')
    promotion = models.OneToOneField(Promotion, on_delete=models.CASCADE, null=True, blank=True, related_name='product_promotion')
    refresh_schedules = models.ManyToManyField(RefreshSchedule, blank=True, related_name='products_refresh_schedules')
    promo_message = models.TextField(null=True, blank=True)
    promo_condition = models.CharField(max_length=255, null=True, blank=True)
    promo_fid_card_message = models.CharField(max_length=255, null=True, blank=True)
    promo_mixing_message = models.TextField(null=True, blank=True)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('store_profile', 'code_article')

    def __str__(self):
        return self.code_article or ''

    def save(self, *args, **kwargs):
        logger.info(f"Saving Product: {self.code_article}")
        super().save(*args, **kwargs)
        logger.info(f"Product saved: {self.code_article}")
