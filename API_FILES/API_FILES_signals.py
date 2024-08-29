# API_FILES/signals.py
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal
from .models import UploadedFile, ParsedData
from Corak_ESL.models import Export2Zkong
from Corak_ESL.Corak_ESL_API import ZkongAPI, ZkongAuth
from custom_user_management.models import Corak_API_userProfile
from django.shortcuts import get_object_or_404

logger = logging.getLogger('api_files')

def delete_products_marked_for_deletion():
    products_to_delete = ParsedData.objects.filter(action='s')
    for product in products_to_delete:
        product.delete()
        logger.info(f"Product with gencod_ean {product.gencod_ean} deleted from ParsedData.")

def collect_and_delete_marked_products():
    products_to_delete = ParsedData.objects.filter(action='s')
    barcodes_to_delete = [product.gencod_ean for product in products_to_delete]

    if barcodes_to_delete:
        for product in products_to_delete:
            product.delete()
            logger.info(f"Product with gencod_ean {product.gencod_ean} deleted from ParsedData.")
    else:
        logger.info("No products marked for deletion.")

def calculate_price_per_unit(measure_unit, content, sale_price):
    price_per_unit_str = ""

    if measure_unit and content and sale_price:
        if measure_unit == 'U':
            conversion_factor = Decimal(1000)
            unit = "Kg"
        elif measure_unit == 'L':
            conversion_factor = Decimal(1000)
            unit = "L"
        else:
            conversion_factor = None

        if conversion_factor:
            quantity_in_unit = Decimal(content) / conversion_factor
            price_per_unit = sale_price / quantity_in_unit
            price_per_unit_str = f"{price_per_unit:.2f}€/{unit}"

    return price_per_unit_str

@receiver(post_save, sender=UploadedFile)
def parse_file(sender, instance, **kwargs):
    if not instance.file:
        logger.error("No file found in UploadedFile instance.")
        return

    try:
        store_profile_instance = Corak_API_userProfile.objects.get(id=instance.store_profile_id)
    except Corak_API_userProfile.DoesNotExist:
        logger.error("Store profile does not exist.")
        return

    user = store_profile_instance.account
    auth = ZkongAuth(user)
    api = ZkongAPI(auth)

    def map_parsed_data_to_export(parsed_data_instance):
        price_per_unit_str = calculate_price_per_unit(parsed_data_instance.measure_unit, parsed_data_instance.content, parsed_data_instance.sale_price)

        export_instance, created = Export2Zkong.objects.update_or_create(
            barCode=parsed_data_instance.gencod_ean,
            store_profile=store_profile_instance,
            defaults={
                'itemTitle': parsed_data_instance.main_label,
                'shortTitle': parsed_data_instance.secondary_label,
                'unit': parsed_data_instance.measure_unit,
                'price': parsed_data_instance.sale_price,
                'custFeature13': parsed_data_instance.content,
                'custFeature2': parsed_data_instance.ug_article,
                'custFeature12': parsed_data_instance.secondary_label,
                'custFeature14': "Top meilleur vente" if parsed_data_instance.top_best_sale == 'onnn' else " " if parsed_data_instance.top_best_sale == 'nnnn' else None,
                'custFeature50': parsed_data_instance.action,
                'custFeature49': parsed_data_instance.sticker_update,
                'custFeature48': parsed_data_instance.presentation_stock,
                'custFeature47': parsed_data_instance.restock_unit,
                'custFeature46': parsed_data_instance.management_data,
                'custFeature45': parsed_data_instance.promotion_status,
            }
        )
        return export_instance, created

    store_profile = instance.store_profile

    encodings = ['utf-8', 'iso-8859-1']

    file_content = None
    for encodage in encodings:
        try:
            with instance.file.open('rb') as file:
                file_content = file.read().decode(encodage)
            break
        except UnicodeDecodeError:
            continue

    if file_content is None:
        logger.error("Error parsing file: Failed to decode the file with provided encodings.")
        return

    try:
        lines = file_content.splitlines()

        for line in lines:
            action = line[0]
            sticker_update = line[1]
            gencod_ean = line[2:15].strip()
            main_label = line[15:45].strip()
            secondary_label = line[45:60].strip()
            measure_unit = line[60]
            content_str = line[61:67].strip()
            if content_str[0] in ['K', 'U', 'L']:
                measure_unit = content_str[0]
                content = int(content_str[1:])
            else:
                measure_unit = line[60]
                content = int(content_str)
            sale_price_str = line[67:72].strip()
            sale_price = Decimal(sale_price_str[:-2] + '.' + sale_price_str[-2:])
            promotion_status = line[72]
            top_best_sale = line[73:77].strip()
            management_data = line[77:83].strip()
            decimal_point = line[83]
            presentation_stock = line[84:89].strip().lstrip('0') or '0'
            restock_unit = line[89:94].strip()
            ug_article = line[94:100].strip()

            data_to_save = {
                'action': action,
                'sticker_update': sticker_update,
                'gencod_ean': gencod_ean,
                'main_label': main_label,
                'secondary_label': secondary_label,
                'measure_unit': measure_unit,
                'content': content,
                'sale_price': sale_price,
                'promotion_status': promotion_status,
                'top_best_sale': top_best_sale,
                'management_data': management_data,
                'decimal_point': decimal_point,
                'presentation_stock': presentation_stock,
                'restock_unit': restock_unit,
                'ug_article': ug_article,
                'store_profile': store_profile
            }

            parsed_data, created = ParsedData.objects.update_or_create(
                gencod_ean=gencod_ean,
                store_profile=store_profile,
                defaults=data_to_save
            )

            export_instance, created = map_parsed_data_to_export(parsed_data)
            export_instance.save()
            logger.info(f"Saved export instance for {gencod_ean}")

            if created:
                logger.info(f"New product with gencod_ean {gencod_ean} created.")
            else:
                logger.info(f"Product with gencod_ean {gencod_ean} updated.")

    except Exception as e:
        logger.error(f"Error parsing file: {e}")

    delete_products_marked_for_deletion()
