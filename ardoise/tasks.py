import logging
from celery import shared_task
from .models import Product, CustomDetail, Certificates, Fresh
from django.utils import timezone

logger = logging.getLogger('ardoise')

@shared_task(name='ardoise.tasks.process_custom_detail')
def process_custom_detail(custom_detail_id):
    try:
        custom_detail = CustomDetail.objects.get(id=custom_detail_id)
        logger.info(f"Processing CustomDetail with ID: {custom_detail_id}")
        # Logique pour traiter le CustomDetail
        # Exemple : mise à jour du produit correspondant
        update_product(custom_detail.store_profile, custom_detail.code_article)
    except CustomDetail.DoesNotExist:
        logger.error(f"CustomDetail with ID {custom_detail_id} does not exist")
    except Exception as e:
        logger.error(f"Error processing CustomDetail {custom_detail_id}: {e}")

@shared_task(name='ardoise.tasks.process_certificates')
def process_certificates(certificates_id):
    try:
        certificates = Certificates.objects.get(id=certificates_id)
        logger.info(f"Processing Certificates with ID: {certificates_id}")
        # Logique pour traiter les Certificates
        # Exemple : mise à jour du produit correspondant
        update_product(certificates.store_profile, certificates.code_article)
    except Certificates.DoesNotExist:
        logger.error(f"Certificates with ID {certificates_id} does not exist")
    except Exception as e:
        logger.error(f"Error processing Certificates {certificates_id}: {e}")

def update_product(store_profile, code_article):
    try:
        product, created = Product.objects.update_or_create(
            store_profile=store_profile,
            code_article=code_article,
            defaults={
                'custom': CustomDetail.objects.filter(store_profile=store_profile, code_article=code_article).first(),
                'certificates': Certificates.objects.filter(store_profile=store_profile, code_article=code_article).first()
            }
        )
        logger.info(f"Product {'created' if created else 'updated'} for code_article: {code_article}")
        # Logique pour mise à jour Export2Zkong ou autre action
    except Exception as e:
        logger.error(f"Error updating product for {code_article}: {e}")
