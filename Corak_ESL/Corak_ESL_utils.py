from .models import Export2Zkong
from API_ITEMS.API_ITEMS_calcs import split_promotion_message  # Assurez-vous que le chemin d'importation est correct
from API_ITEMS.models import Product
from django.db import transaction
import logging
import requests
import json
import os

logger = logging.getLogger('corak_esl')

def update_export2zkong_from_product(product_instance):
    # Mettre à jour Export2Zkong avec les données de product_instance
    try:
        logger.info(f"Updating Export2Zkong for product {product_instance.code_article} in store {product_instance.store_profile.store_number}")
        
        # Utiliser la fonction split_promotion_message pour obtenir les détails de la promotion
        discount, _, details = split_promotion_message(product_instance.promo_message)

        promotion_start = product_instance.promotion.start.strftime(
            "%Y-%m-%d %H:%M:%S") if product_instance.promotion and product_instance.promotion.start else None
        promotion_end = product_instance.promotion.end.strftime(
            "%Y-%m-%d %H:%M:%S") if product_instance.promotion and product_instance.promotion.end else None

        export2zkong = Export2Zkong.objects.filter(barCode=product_instance.code_article).first()

        if not export2zkong:
            logger.warning(f"Product {product_instance.code_article} not found in store {product_instance.store_profile.store_number}")
            return f"Produit inconnu dans ce magasin: {product_instance.code_article}"

        export2zkong.store_profile = product_instance.store_profile
        export2zkong.proStartTime = promotion_start
        export2zkong.proEndTime = promotion_end
        export2zkong.promotionText = product_instance.promo_message
        export2zkong.custFeature8 = product_instance.promo_condition
        export2zkong.custFeature9 = product_instance.promo_fid_card_message
        export2zkong.custFeature7 = product_instance.promo_mixing_message
        export2zkong.custFeature6 = discount
        # ... autres champs ...

        export2zkong.save()
        logger.info(f"Successfully updated Export2Zkong for product {product_instance.code_article}")
        return None  # Indique que la mise à jour a été réussie

    except Exception as e:
        logger.error(f"Error updating Export2Zkong: {e}")
        return f"Erreur de mise à jour pour le produit {product_instance.code_article} dans le magasin {product_instance.store_profile.store_number}"
