# signals.py

import json
import logging
import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import UploadedFile
from API_ITEMS.models import Custom, Promotion, RefreshSchedule
from API_ITEMS.API_ITEMS_serializers import CustomSerializer, PromotionSerializer, RefreshScheduleSerializer
from custom_user_management.models import Corak_API_userProfile
from rest_framework.exceptions import ValidationError
from API_ITEMS.API_ITEMS_signals import create_or_update_product

logger = logging.getLogger('common')

@receiver(post_save, sender=UploadedFile)
def process_promo_file(sender, instance, created, **kwargs):
    if created and instance.file_type == 'Promo':
        try:
            file_path = os.path.join(settings.MEDIA_ROOT, instance.file.name)
            if not os.path.exists(file_path):
                logger.error(f"File {file_path} does not exist.")
                return

            with open(file_path, 'r') as file:
                content = file.read()
                data = json.loads(content)

            for item in data:
                store_profile = instance.store_profile
                if not isinstance(store_profile, Corak_API_userProfile):
                    store_profile = Corak_API_userProfile.objects.get(id=store_profile)

                code_article = item['id']

                # Process Custom data
                custom_data = item.get('custom', {})
                if custom_data:
                    custom_data['store_profile'] = store_profile
                    custom_data['code_article'] = code_article
                    # Convert necessary fields to integers
                    if 'ADVCARACT_MIN' in custom_data:
                        custom_data['ADVCARACT_MIN'] = int(custom_data['ADVCARACT_MIN'])
                    if 'ADVTYPE_ID' in custom_data:
                        custom_data['ADVTYPE_ID'] = int(custom_data['ADVTYPE_ID'])
                    if 'ADVCARACT_AMOUNT' in custom_data:
                        custom_data['ADVCARACT_AMOUNT'] = int(custom_data['ADVCARACT_AMOUNT'])
                    custom_serializer = CustomSerializer(data=custom_data)
                    if custom_serializer.is_valid():
                        custom_serializer.save()
                    else:
                        Custom.objects.update_or_create(
                            code_article=code_article,
                            store_profile=store_profile,
                            defaults=custom_data
                        )

                # Process Promotion data
                promotion_data = item.get('promotion', {})
                if promotion_data:
                    promotion_data['store_profile'] = store_profile
                    promotion_data['code_article'] = code_article
                    promotion_serializer = PromotionSerializer(data=promotion_data)
                    if promotion_serializer.is_valid():
                        promotion_serializer.save()
                    else:
                        Promotion.objects.update_or_create(
                            code_article=code_article,
                            store_profile=store_profile,
                            defaults=promotion_data
                        )

                # Process RefreshSchedule data
                refresh_schedules_data = item.get('refreshSchedules', [])
                for schedule in refresh_schedules_data:
                    schedule_data = {
                        'store_profile': store_profile,
                        'code_article': code_article,
                        'date': schedule
                    }
                    refresh_schedule_serializer = RefreshScheduleSerializer(data=schedule_data)
                    if refresh_schedule_serializer.is_valid():
                        refresh_schedule_serializer.save()
                    else:
                        RefreshSchedule.objects.update_or_create(
                            code_article=code_article,
                            store_profile=store_profile,
                            defaults={'date': schedule}
                        )

                # Créer ou mettre à jour le produit
                create_or_update_product(store_profile, code_article)

            logger.info(f"Processed Promo file {instance.file.name} successfully.")

        except Exception as e:
            logger.error(f"Error processing Promo file {instance.file.name}: {e}")

# Ajout du traitement pour les fichiers Ardoise
from ardoise.models import CustomDetail, Certificates, Fresh, Product
from ardoise.ardoise_serializers import CustomDetailSerializer, CertificateDetailSerializer, FreshSerializer, ProductSerializer

@receiver(post_save, sender=UploadedFile)
def process_ardoise_file(sender, instance, created, **kwargs):
    if created and instance.file_type == 'Ardoise':
        try:
            file_path = os.path.join(settings.MEDIA_ROOT, instance.file.name)
            if not os.path.exists(file_path):
                logger.error(f"File {file_path} does not exist.")
                return

            with open(file_path, 'r') as file:
                content = file.read()
                data = json.loads(content)

            for item in data:
                store_profile = instance.store_profile
                if not isinstance(store_profile, Corak_API_userProfile):
                    store_profile = Corak_API_userProfile.objects.get(id=store_profile)

                code_article = item['id']

                # Process CustomDetail data
                custom_detail_data = item.get('custom', {})
                custom_instance = None
                if custom_detail_data:
                    custom_detail_data['store_profile'] = store_profile
                    custom_detail_data['code_article'] = code_article
                    custom_detail_serializer = CustomDetailSerializer(data=custom_detail_data)
                    if custom_detail_serializer.is_valid():
                        custom_instance = custom_detail_serializer.save()
                    else:
                        custom_instance, _ = CustomDetail.objects.update_or_create(
                            code_article=code_article,
                            store_profile=store_profile,
                            defaults=custom_detail_data
                        )

                # Process Certificates data
                certificates_data = item.get('certificates', {})
                certificates_instance = None
                if certificates_data:
                    certificates_data['store_profile'] = store_profile
                    certificates_data['code_article'] = code_article
                    certificates_serializer = CertificateDetailSerializer(data=certificates_data)
                    if certificates_serializer.is_valid():
                        certificates_instance = certificates_serializer.save()
                    else:
                        certificates_instance, _ = Certificates.objects.update_or_create(
                            code_article=code_article,
                            store_profile=store_profile,
                            defaults=certificates_data
                        )

                # Process Fresh data
                fresh_data = item.get('fresh', {})
                fresh_instance = None
                if fresh_data:
                    fresh_data['store_profile'] = store_profile
                    fresh_data['code_article'] = code_article
                    fresh_serializer = FreshSerializer(data=fresh_data)
                    if fresh_serializer.is_valid():
                        fresh_instance = fresh_serializer.save()
                    else:
                        fresh_instance, _ = Fresh.objects.update_or_create(
                            code_article=code_article,
                            store_profile=store_profile,
                            defaults=fresh_data
                        )

                # Process Product data
                product_data = {
                    'store_profile': store_profile,
                    'code_article': code_article,
                    'price': item.get('price'),
                    'unitPriceUnit': item.get('unitPriceUnit'),
                    'currency': item.get('currency'),
                    'capacity': item.get('capacity'),
                    'custom': custom_instance,
                    'certificates': certificates_instance,
                }

                product_serializer = ProductSerializer(data=product_data, context={'store_profile': store_profile})
                if product_serializer.is_valid():
                    product_serializer.save()
                else:
                    Product.objects.update_or_create(
                        code_article=code_article,
                        store_profile=store_profile,
                        defaults=product_data
                    )

            logger.info(f"Processed Ardoise file {instance.file.name} successfully.")

        except Exception as e:
            logger.error(f"Error processing Ardoise file {instance.file.name}: {e}")
