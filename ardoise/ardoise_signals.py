import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from ardoise.models import Product, CustomDetail, Certificates
from Corak_ESL.models import Export2Zkong
from custom_user_management.models import Corak_API_userProfile

# Configuration du logger pour l'application ardoise
logger = logging.getLogger('ardoise')

@receiver(post_save, sender=Product)
def on_product_save(sender, instance, **kwargs):
    # Extraction des données du produit et des modèles associés
    product_data = {
        "barCode": instance.code_article,
        "price": instance.price,
        "custFeature15": instance.capacity,
        "custFeature16": instance.unitPriceUnit,
        "custFeature17": instance.currency
    }

    if instance.custom:
        product_data.update({
            "shortTitle": instance.custom.libelle_cr_auto,
            "itemTitle": instance.custom.libelle_lg_auto,
            "custFeature18": instance.custom.geeti1_auto,
            "custFeature19": instance.custom.type_auto,
            "custFeature20": instance.custom.traitement_auto,
            "custFeature21": instance.custom.conditionnement_auto,
            "custFeature22": instance.custom.certifie_auto,
            "custFeature23": instance.custom.fresh_origine_BO,
            "custFeature24": instance.custom.fresh_caliber_BO,
            "custFeature25": instance.custom.fresh_category_BO,
            "custFeature26": instance.custom.fresh_variety_BO,
            "custFeature27": instance.custom.promo_gold_auto,  # Ajout du champ promo_gold_auto
            "attrName": "Fruits&Légumes",
            "attrCategory": "Ardoise"
        })

    if instance.certificates:
        product_data.update({
            "custFeature27": instance.certificates.fairTrade,
            "custFeature28": instance.certificates.organic,
            "custFeature29": instance.certificates.environmentallyFriendly
        })

    # Vérifiez que l'instance de Product a un store_profile associé avant de tenter la mise à jour
    if instance.store_profile:
        logger.info(f"Updating or creating Export2Zkong entry for product: {instance.code_article} in store: {instance.store_profile.store_number}")
        Export2Zkong.objects.update_or_create(
            barCode=instance.code_article,
            store_profile=instance.store_profile,
            defaults=product_data
        )
    else:
        logger.warning(f"Product {instance.code_article} does not have a store_profile associated. Skipping Export2Zkong update.")

@receiver(post_delete, sender=Product)
def on_product_delete(sender, instance, **kwargs):
    logger.info(f"Deleting Export2Zkong entry for product: {instance.code_article}")
    # Suppression de l'entrée correspondante dans Export2Zkong
    Export2Zkong.objects.filter(barCode=instance.code_article).delete()
