from celery import shared_task
from django.utils import timezone
import logging
from .models import Product, Export2Zkong
from .zkong_api import send_to_zkong  # Assurez-vous d'avoir un module pour l'envoi à l'API ZKONG

logger = logging.getLogger('corak_esl')

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_products_to_zkong(self):
    logger.info("Starting send_products_to_zkong task")
    try:
        process_batches()
        logger.info("Completed send_products_to_zkong task")
    except Exception as e:
        logger.error(f"Error in send_products_to_zkong task: {e}")

def process_batches():
    batch_size = 20000
    products = Export2Zkong.objects.all()
    total_products = products.count()
    logger.info(f"Total products to send: {total_products}")
    
    for start in range(0, total_products, batch_size):
        end = min(start + batch_size, total_products)
        batch = products[start:end]
        logger.info(f"Processing batch from {start} to {end}")
        
        formatted_batch = format_batch(batch)
        send_to_zkong(formatted_batch)
        logger.info(f"Batch from {start} to {end} processed successfully")

def format_batch(batch):
    formatted_batch = []
    for product in batch:
        product_data = {
            "store_profile": product.store_profile,
            "barCode": product.barCode,
            "attrCategory": product.attrCategory,
            "attrName": product.attrName,
            "productCode": product.productCode,
            "productSku": product.productSku,
            "itemTitle": product.itemTitle,
            "shortTitle": product.shortTitle,
            "classLevel": product.classLevel,
            "productArea": product.productArea,
            "unit": product.unit,
            "qrCode": product.qrCode,
            "nfcUrl": product.nfcUrl,
            "spec": product.spec,
            "originalPrice": str(product.originalPrice) if product.originalPrice else None,
            "price": str(product.price) if product.price else None,
            "memberPrice": str(product.memberPrice) if product.memberPrice else None,
            "stock1": str(product.stock1) if product.stock1 else None,
            "stock2": str(product.stock2) if product.stock2 else None,
            "stock3": str(product.stock3) if product.stock3 else None,
            "proStartTime": product.proStartTime if product.proStartTime else None,
            "proEndTime": product.proEndTime if product.proEndTime else None,
            "promotionText": product.promotionText,
            "custFeature1": product.custFeature1,
            "custFeature2": product.custFeature2,
            "custFeature3": product.custFeature3,
        }
        formatted_batch.append(product_data)
    logger.info(f"Formatted batch of {len(formatted_batch)} products")
    return formatted_batch
