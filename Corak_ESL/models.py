from django.db import models
from decimal import Decimal, ROUND_HALF_UP
import re
from custom_user_management.models import Corak_API_userProfile
import logging

logger = logging.getLogger('corak_esl')


# Le modèle Article représente une table dans la base de données.
class Export2Zkong(models.Model):
    store_profile = models.ForeignKey(Corak_API_userProfile, on_delete=models.CASCADE, related_name='export2zkong_items', null=True, blank=True)
    barCode = models.CharField(max_length=100, null=True,
                               blank=True)  # Unique car chaque code-barres devrait être distinct.
    attrCategory = models.CharField(max_length=100, default="default", null=True, blank=True)
    attrName = models.CharField(max_length=100, default="default", null=True, blank=True)
    productCode = models.CharField(max_length=100, null=True, blank=True)
    productSku = models.CharField(max_length=100, null=True, blank=True)
    itemTitle = models.CharField(max_length=100, null=True, blank=True)
    shortTitle = models.CharField(max_length=100, null=True, blank=True)
    classLevel = models.CharField(max_length=100, null=True, blank=True)
    productArea = models.CharField(max_length=100, null=True, blank=True)
    unit = models.CharField(max_length=100, null=True, blank=True)
    qrCode = models.CharField(max_length=100, null=True, blank=True)
    nfcUrl = models.CharField(max_length=100, null=True, blank=True)
    spec = models.CharField(max_length=100, null=True, blank=True)
    originalPrice = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    memberPrice = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock1 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock2 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock3 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    proStartTime = models.CharField(max_length=100, null=True, blank=True)
    proEndTime = models.CharField(max_length=100, null=True, blank=True)
    promotionText = models.CharField(max_length=100, null=True, blank=True)
    custFeature1 = models.CharField(max_length=100, null=True, blank=True)
    custFeature2 = models.CharField(max_length=100, null=True, blank=True)
    custFeature3 = models.CharField(max_length=100, null=True, blank=True)
    custFeature4 = models.CharField(max_length=100, null=True, blank=True)
    custFeature5 = models.CharField(max_length=100, null=True, blank=True)
    custFeature6 = models.CharField(max_length=100, null=True, blank=True)
    custFeature7 = models.CharField(max_length=100, null=True, blank=True)
    custFeature8 = models.CharField(max_length=100, null=True, blank=True)
    custFeature9 = models.CharField(max_length=100, null=True, blank=True)
    custFeature10 = models.CharField(max_length=100, null=True, blank=True)
    custFeature11 = models.CharField(max_length=100, null=True, blank=True)
    custFeature12 = models.CharField(max_length=100, null=True, blank=True)
    custFeature13 = models.CharField(max_length=100, null=True, blank=True)
    custFeature14 = models.CharField(max_length=100, null=True, blank=True)
    custFeature15 = models.CharField(max_length=100, null=True, blank=True)
    custFeature16 = models.CharField(max_length=100, null=True, blank=True)
    custFeature17 = models.CharField(max_length=100, null=True, blank=True)
    custFeature18 = models.CharField(max_length=100, null=True, blank=True)
    custFeature19 = models.CharField(max_length=100, null=True, blank=True)
    custFeature20 = models.CharField(max_length=100, null=True, blank=True)
    custFeature21 = models.CharField(max_length=100, null=True, blank=True)
    custFeature22 = models.CharField(max_length=100, null=True, blank=True)
    custFeature23 = models.CharField(max_length=100, null=True, blank=True)
    custFeature24 = models.CharField(max_length=100, null=True, blank=True)
    custFeature25 = models.CharField(max_length=100, null=True, blank=True)
    custFeature26 = models.CharField(max_length=100, null=True, blank=True)
    custFeature27 = models.CharField(max_length=100, null=True, blank=True)
    custFeature28 = models.CharField(max_length=100, null=True, blank=True)
    custFeature29 = models.CharField(max_length=100, null=True, blank=True)
    custFeature30 = models.CharField(max_length=100, null=True, blank=True)
    custFeature31 = models.CharField(max_length=100, null=True, blank=True)
    custFeature32 = models.CharField(max_length=100, null=True, blank=True)
    custFeature33 = models.CharField(max_length=100, null=True, blank=True)
    custFeature34 = models.CharField(max_length=100, null=True, blank=True)
    custFeature35 = models.CharField(max_length=100, null=True, blank=True)
    custFeature36 = models.CharField(max_length=100, null=True, blank=True)
    custFeature37 = models.CharField(max_length=100, null=True, blank=True)
    custFeature38 = models.CharField(max_length=100, null=True, blank=True)
    custFeature39 = models.CharField(max_length=100, null=True, blank=True)
    custFeature40 = models.CharField(max_length=100, null=True, blank=True)
    custFeature41 = models.CharField(max_length=100, null=True, blank=True)
    custFeature42 = models.CharField(max_length=100, null=True, blank=True)
    custFeature43 = models.CharField(max_length=100, null=True, blank=True)
    custFeature44 = models.CharField(max_length=100, null=True, blank=True)
    custFeature45 = models.CharField(max_length=100, null=True, blank=True)
    custFeature46 = models.CharField(max_length=100, null=True, blank=True)
    custFeature47 = models.CharField(max_length=100, null=True, blank=True)
    custFeature48 = models.CharField(max_length=100, null=True, blank=True)
    custFeature49 = models.CharField(max_length=100, null=True, blank=True)
    custFeature50 = models.CharField(max_length=100, null=True, blank=True)
    custFeature51 = models.CharField(max_length=100, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('barCode', 'store_profile',)  # Définition de l'unicité combinée
    # Cette méthode permet d'afficher une représentation textuelle d'un article.
    def __str__(self):
        return self.barCode or self.itemTitle or 'Nom non défini'

    def calculate_discounted_price(self):
        logger.info(
            f"Calculating discounted price for {self.barCode} with price {self.price} and discount {self.custFeature6}")

        if self.custFeature6:
            discount_info = self.custFeature6
            # Gestion du pourcentage
            percent_match = re.match(r"(\d+(?:\.\d+)?)%", discount_info)
            if percent_match:
                discount_rate = Decimal(percent_match.group(1)) / Decimal('100')
                discounted_price = (self.price * (Decimal('1') - discount_rate)).quantize(Decimal('.01'),
                                                                                          rounding=ROUND_HALF_UP)
                logger.info(f"Percentage discount applied: {discount_rate * 100}%, discounted price: {discounted_price}")
                return discounted_price

            # Gestion de l'euro
            euro_match = re.match(r"(\d+(?:\.\d+)?)€", discount_info)
            if euro_match:
                discount_amount = Decimal(euro_match.group(1))
                discounted_price = (self.price - discount_amount).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
                logger.info(f"Euro discount applied: {discount_amount}€, discounted price: {discounted_price}")
                return discounted_price

            # Gestion de la promotion 'n+n offerts'
            nn_match = re.match(r"(\d+)\+(\d+)", discount_info)
            if nn_match:
                n1, n2 = int(nn_match.group(1)), int(nn_match.group(2))
                discounted_price = ((self.price * Decimal(n1)) / Decimal(n1 + n2)).quantize(Decimal('.01'),
                                                                                            rounding=ROUND_HALF_UP)
                logger.info(f"'n+n' discount applied: {n1}+{n2}, discounted price per unit: {discounted_price}")
                return discounted_price

            # Si le format de remise est inconnu
            logger.info(f"Unknown discount format: {discount_info}")

        logger.info("No discount information provided or recognized.")
        return self.price

    def save(self, *args, **kwargs):
        # Assurez-vous que 'price' n'est pas None avant de calculer le prix remisé
        if self.price is not None:
            self.memberPrice = self.calculate_discounted_price()
        super().save(*args, **kwargs)
    def get_discounted_price_str(self):
        discounted_price = self.calculate_discounted_price()
        return "{:.2f}".format(discounted_price) if discounted_price else None

class ZkongLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    level = models.CharField(max_length=10)
    message = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)  # Met à jour le champ à chaque sauvegarde de l'objet

    def __str__(self):
        return f"{self.timestamp} - {self.level} - {self.message}"
