from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import model_to_dict
from django.core.signals import request_finished
from .models import Export2Zkong
from .Corak_ESL_API import ZkongAPI, ZkongAuth, BatchDelete
from custom_user_management.models import Corak_API_userProfile
import json
from decimal import Decimal
import logging

logger = logging.getLogger('corak_esl')

# Liste globale pour stocker les articles mis à jour
updated_articles = []

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)

@receiver(post_save, sender=Export2Zkong)
def export2zkong_post_save(sender, instance, created, **kwargs):
    global updated_articles

    # Convertir les données de l'instance en JSON
    article_data = model_to_dict(instance, exclude=["id"])
    article_data_json = json.dumps(article_data, default=decimal_default)

    # Ajouter l'article à la liste des mises à jour
    updated_articles.append(article_data_json)

    logger.info(f"Article {instance.barCode} ajouté à la liste des mises à jour.")

@receiver(request_finished)
def send_batch_update(sender, **kwargs):
    global updated_articles

    if updated_articles:
        # Obtenez l'utilisateur à partir de la première instance (hypothèse que tous les articles mis à jour appartiennent au même utilisateur)
        first_article = json.loads(updated_articles[0])
        store_profile_id = first_article.get('store_profile')
        store_profile_instance = Corak_API_userProfile.objects.get(id=store_profile_id)
        user = store_profile_instance.account

        # Initialisez auth et api avec l'utilisateur spécifique
        auth = ZkongAuth(user)
        zkong_api = ZkongAPI(auth)
        batch_delete_api = BatchDelete(auth)

        logger.info("Envoi des articles mis à jour à Zkong...")

        # Ajouter tous les articles mis à jour à l'API
        for article_data_json in updated_articles:
            zkong_api.add_updated_article(article_data_json)

        # Déclencher la mise à jour en lot
        zkong_api.batch_import_updated_articles()

        # Réinitialisez la liste après l'envoi
        updated_articles = []

        # Récupérer tous les produits nécessitant la suppression
        products_to_delete = [
            prod.barCode for prod in Export2Zkong.objects.filter(custFeature50='s')
            if prod.barCode not in deleted_products
        ]

        # Effectuer la suppression en lot si la liste n'est pas vide
        if products_to_delete:
            delete_response = batch_delete_api.execute_batch_delete(products_to_delete)
            logger.info(delete_response)

            # Mettre à jour le set des produits supprimés
            if "successful" in delete_response:
                deleted_products.update(products_to_delete)

        logger.info("Mise à jour en lot envoyée et produits marqués pour suppression traités.")
    else:
        logger.info("Aucune mise à jour à envoyer.")
