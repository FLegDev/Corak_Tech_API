from celery import shared_task
from django.utils import timezone
import logging
from .models import RefreshSchedule, Product
from .API_ITEMS_signals import update_export2zkong

logger = logging.getLogger('api_items')

@shared_task(name='API_ITEMS.tasks.test_check_and_update_promotions', bind=True, max_retries=3, default_retry_delay=60)
def test_check_and_update_promotions(self):
    logger.info("Starting test_check_and_update_promotions task")
    try:
        refresh_product_schedules()
        logger.info("Completed test_check_and_update_promotions task")
    except Exception as e:
        logger.error(f"Error in test_check_and_update_promotions task: {e}")

@shared_task(name='API_ITEMS.tasks.refresh_product_schedules', bind=True, max_retries=5, default_retry_delay=60)
def refresh_product_schedules(self):
    logger.info("Starting refresh_product_schedules task")
    try:
        current_datetime = timezone.now()
        schedules = RefreshSchedule.objects.filter(date__date=current_datetime.date())
        schedule_data = []

        for schedule in schedules:
            schedule_info = {
                'store_profile': schedule.store_profile.store_number,
                'code_article': schedule.code_article,
                'date': schedule.date.isoformat()
            }
            schedule_data.append(schedule_info)
            logger.info(f"RefreshSchedule: {schedule_info}")

            product = schedule.product
            if product and product.promotion:
                promotion = product.promotion
                apply_delta(promotion)
                promotion.update_status()

                logger.info(f"Promotion mise à jour pour {promotion.code_article}: active={promotion.is_active}")

                if promotion.start <= current_datetime <= promotion.end:
                    product.promotion_data_in_zkong = promotion
                    logger.info(f"Promotion active pour le produit {product.code_article}")
                else:
                    product.promotion_data_in_zkong = None
                    logger.info(f"Promotion inactive pour le produit {product.code_article}")

                product.save()
                try:
                    update_export2zkong(product)
                    logger.info(f"Product {product.code_article} updated in Export2Zkong")
                except Exception as e:
                    logger.error(f"Error updating Export2Zkong for product {product.code_article}: {e}")

        logger.info("Completed refreshing product schedules and updating promotions.")
        return schedule_data

    except Exception as e:
        logger.exception("Error fetching refresh schedules")
        self.retry(exc=e, countdown=60)
        return []

def apply_delta(promotion):
    if promotion.product and promotion.product.custom:
        adv_active = promotion.product.custom.ADV_ACTIVE
        if adv_active == '0':
            promotion.end = timezone.now()
            promotion.save()
            logger.info(f"Promotion {promotion.code_article} désactivée car ADV_ACTIVE est 0.")
        else:
            logger.info(f"Promotion {promotion.code_article} active.")
