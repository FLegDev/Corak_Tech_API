import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import Custom, Promotion, Product, RefreshSchedule
from .API_ITEMS_calcs import handle_custom_save, determine_message, get_promotion_times_as_string
from Corak_ESL.Corak_ESL_utils import update_export2zkong_from_product

logger = logging.getLogger(__name__)

def create_or_update_product(store_profile, code_article):
    try:
        logger.info(f"Starting create_or_update_product for code_article: {code_article}, store_profile: {store_profile}")

        custom_instance = Custom.objects.filter(code_article=code_article, store_profile=store_profile).first()
        promotion_instance = Promotion.objects.filter(code_article=code_article, store_profile=store_profile).first()
        refresh_schedules_instances = RefreshSchedule.objects.filter(code_article=code_article, store_profile=store_profile)

        logger.info(f"Custom instance: {custom_instance}")
        logger.info(f"Promotion instance: {promotion_instance}")
        logger.info(f"Refresh Schedules instances: {list(refresh_schedules_instances)}")

        if custom_instance and promotion_instance:
            advantage, condition, message_fid, info_panachage = determine_message(custom_instance)
            pro_start_time_str, pro_end_time_str = get_promotion_times_as_string(promotion_instance)
            discount_value = custom_instance.ADVCARACT_AMOUNT or 0.0

            logger.info(f"Determined messages - Advantage: {advantage}, Condition: {condition}, Message Fid: {message_fid}, Info Panachage: {info_panachage}")
            logger.info(f"Discount Value: {discount_value}")

            product, created = Product.objects.update_or_create(
                store_profile=store_profile,
                code_article=code_article,
                defaults={
                    'custom': custom_instance,
                    'promotion': promotion_instance,
                    'promo_message': advantage,
                    'promo_condition': condition,
                    'promo_fid_card_message': message_fid,
                    'promo_mixing_message': info_panachage,
                    'discount_value': discount_value,
                }
            )

            product.refresh_schedules.set(refresh_schedules_instances)
            product.save()

            logger.info(f"Updated Product {product.id} with refresh schedules: {list(refresh_schedules_instances)}")

            # Logique pour mise à jour Export2Zkong
            update_export2zkong(product)

    except Exception as e:
        logger.error(f"Error creating or updating Product for {code_article} in store {store_profile.store_number}: {e}")

def update_export2zkong(product):
    try:
        current_date = timezone.now().date()
        refresh_schedules = product.refresh_schedules.all()

        promotion_active = False
        for rs in refresh_schedules:
            if rs.start_date <= current_date <= rs.end_date:
                promotion_active = True
                product.promotion_data_in_zkong = product.promotion
                break

        if not promotion_active:
            product.promotion_data_in_zkong = None

        product.save()
        update_export2zkong_from_product(product)
    except Exception as e:
        logger.error(f"Error updating Export2Zkong: {e}")

@receiver(post_save, sender=Custom)
def custom_post_save(sender, instance, created, **kwargs):
    """
    Mettre à jour l'objet Custom et les produits associés.
    """
    handle_custom_save(instance, created)
    create_or_update_product(instance.store_profile, instance.code_article)

@receiver(post_delete, sender=Custom)
def post_delete_custom(sender, instance, **kwargs):
    try:
        products = Product.objects.filter(custom=instance)
        for product in products:
            product.delete()
    except Product.DoesNotExist:
        pass

@receiver(post_save, sender=Promotion)
def promotion_post_save(sender, instance, **kwargs):
    create_or_update_product(instance.store_profile, instance.code_article)

@receiver(post_delete, sender=Promotion)
def post_delete_promotion(sender, instance, **kwargs):
    try:
        products = Product.objects.filter(promotion=instance)
        for product in products:
            product.delete()
    except Product.DoesNotExist:
        pass

@receiver(post_save, sender=RefreshSchedule)
def refresh_schedule_post_save(sender, instance, **kwargs):
    create_or_update_product(instance.store_profile, instance.code_article)

@receiver(post_delete, sender=RefreshSchedule)
def post_delete_refresh_schedule(sender, instance, **kwargs):
    try:
        products = Product.objects.filter(refresh_schedules=instance)
        for product in products:
            product.refresh_schedules.remove(instance)
    except Product.DoesNotExist:
        pass

@receiver(post_save, sender=Product)
def product_post_save(sender, instance, **kwargs):
    try:
        update_export2zkong_from_product(instance)
    except Exception as e:
        logger.error(f"Error updating Export2Zkong: {e}")
