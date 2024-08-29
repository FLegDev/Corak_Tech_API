from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from custom_user_management.models import Corak_API_userProfile

class Fresh(models.Model):
    store_profile = models.ForeignKey(Corak_API_userProfile, on_delete=models.CASCADE, related_name='Fresh', null=True)
    code_article = models.CharField(max_length=255, null=True, blank=True)
    origine_BO = models.CharField(max_length=255, blank=True, null=True)
    caliber_BO = models.CharField(max_length=255, blank=True, null=True)
    category_BO = models.CharField(max_length=255, blank=True, null=True)
    variety_BO = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('code_article', 'store_profile')  # Assure l'unicité pour cette combinaison de champs

    def __str__(self):
        return f"Fresh: Origine: {self.origine_BO}, Caliber: {self.caliber_BO}"


class Certificates(models.Model):
    store_profile = models.ForeignKey(Corak_API_userProfile, on_delete=models.CASCADE, related_name='Certificates', null=True)
    product = models.OneToOneField('Product', on_delete=models.CASCADE, related_name='related_certificates', null=True,
                                   blank=True)
    code_article = models.CharField(max_length=255, null=True)
    fairTrade = models.BooleanField(default=False)
    organic = models.BooleanField(default=False)
    environmentallyFriendly = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('code_article', 'store_profile')  # Assure l'unicité pour cette combinaison de champs

    def __str__(self):
        return f"Certificates: Fair Trade: {self.fairTrade}, Organic: {self.organic}, Environmentally Friendly: {self.environmentallyFriendly}"

class CustomDetail(models.Model):
    store_profile = models.ForeignKey(Corak_API_userProfile, on_delete=models.CASCADE, related_name='CustomDetail', null=True)
    product = models.OneToOneField('Product', on_delete=models.CASCADE, related_name='related_custom', null=True,
                                   blank=True)
    code_article = models.CharField(max_length=255, null=True)
    lib_unit_auto = models.CharField(max_length=255, blank=True, null=True)
    libelle_cr_auto = models.CharField(max_length=255, blank=True, null=True)
    libelle_lg_auto = models.CharField(max_length=255, blank=True, null=True)
    geeti1_auto = models.CharField(max_length=255, blank=True, null=True)
    type_auto = models.CharField(max_length=255, blank=True, null=True)
    traitement_auto = models.CharField(max_length=255, blank=True, null=True)
    conditionnement_auto = models.CharField(max_length=255, blank=True, null=True)
    certifie_auto = models.CharField(max_length=255, blank=True, null=True)
    fresh_origine_BO = models.CharField(max_length=255, blank=True, null=True)
    fresh_caliber_BO = models.CharField(max_length=255, blank=True, null=True)
    fresh_category_BO = models.CharField(max_length=255, blank=True, null=True)
    fresh_variety_BO = models.CharField(max_length=255, blank=True, null=True)
    promo_gold_auto = models.CharField(max_length=255, blank=True, null=True)  # Add this line
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('code_article', 'store_profile')  # Assure l'unicité pour cette combinaison de champs


    def __str__(self):
        return self.libelle_cr_auto

class Product(models.Model):
    store_profile = models.ForeignKey(Corak_API_userProfile, on_delete=models.CASCADE, related_name='Product', null=True)
    code_article = models.CharField(max_length=255, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField( null=True, blank=True)
    UNIT_CHOICES = [('U', 'Unité'), ('K', 'Kilogramme')]
    unitPriceUnit = models.CharField(max_length=1, choices=UNIT_CHOICES)
    currency = models.CharField(max_length=5)
    custom = models.ForeignKey(CustomDetail, on_delete=models.SET_NULL, null=True, blank=True, related_name="product_details")
    certificates = models.ForeignKey(Certificates, on_delete=models.SET_NULL, null=True, blank=True, related_name="product_certificates")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('code_article', 'store_profile')  # Assure l'unicité pour cette combinaison de champs

    def price_per_kilo(self):
        if self.unitPriceUnit == 'K':
            return self.price
        return self.price * (1000 / self.capacity)

    def __str__(self):
        if self.custom:
            return self.custom.libelle_cr_auto
        return self.code_article or ''
        
@receiver(post_save, sender=CustomDetail)
def update_product_on_custom_save(sender, instance, **kwargs):
    Product.objects.filter(code_article=instance.code_article).update(custom=instance)


@receiver(post_save, sender=Certificates)
def update_product_on_promotion_save(sender, instance, **kwargs):
    Product.objects.filter(code_article=instance.code_article).update(certificates=instance)


