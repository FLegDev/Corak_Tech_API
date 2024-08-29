# API_ITEMS/API_ITEMS_serializers.py
import logging
from rest_framework import serializers
from .models import Custom, Promotion, Product, RefreshSchedule
from custom_user_management.models import Corak_API_userProfile

logger = logging.getLogger(__name__)

class CustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Custom
        fields = '__all__'

    def create(self, validated_data):
        store_profile = validated_data.get('store_profile')
        if not isinstance(store_profile, Corak_API_userProfile):
            store_profile = Corak_API_userProfile.objects.get(id=store_profile)
            validated_data['store_profile'] = store_profile

        instance, created = Custom.objects.update_or_create(
            store_profile=validated_data.get('store_profile'),
            code_article=validated_data.get('code_article'),
            defaults=validated_data
        )
        if created:
            logger.info(f"Created new Custom instance for store_profile {store_profile.id} and code_article {validated_data.get('code_article')}")
        else:
            logger.info(f"Updated existing Custom instance for store_profile {store_profile.id} and code_article {validated_data.get('code_article')}")
        return instance

    def update(self, instance, validated_data):
        store_profile = validated_data.get('store_profile')
        if not isinstance(store_profile, Corak_API_userProfile):
            store_profile = Corak_API_userProfile.objects.get(id=store_profile)
            validated_data['store_profile'] = store_profile

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        logger.info(f"Updated Custom instance for store_profile {store_profile.id} and code_article {instance.code_article}")
        return instance

class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = '__all__'

    def create(self, validated_data):
        store_profile = validated_data.get('store_profile')
        if not isinstance(store_profile, Corak_API_userProfile):
            store_profile = Corak_API_userProfile.objects.get(id=store_profile)
            validated_data['store_profile'] = store_profile

        instance, created = Promotion.objects.update_or_create(
            store_profile=validated_data.get('store_profile'),
            code_article=validated_data.get('code_article'),
            defaults=validated_data
        )
        if created:
            logger.info(f"Created new Promotion instance for store_profile {store_profile.id} and code_article {validated_data.get('code_article')}")
        else:
            logger.info(f"Updated existing Promotion instance for store_profile {store_profile.id} and code_article {validated_data.get('code_article')}")
        return instance

    def update(self, instance, validated_data):
        store_profile = validated_data.get('store_profile')
        if not isinstance(store_profile, Corak_API_userProfile):
            store_profile = Corak_API_userProfile.objects.get(id=store_profile)
            validated_data['store_profile'] = store_profile

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        logger.info(f"Updated Promotion instance for store_profile {store_profile.id} and code_article {instance.code_article}")
        return instance

class RefreshScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefreshSchedule
        fields = '__all__'

    def create(self, validated_data):
        store_profile = validated_data.get('store_profile')
        if not isinstance(store_profile, Corak_API_userProfile):
            store_profile = Corak_API_userProfile.objects.get(id=store_profile)
            validated_data['store_profile'] = store_profile

        instance, created = RefreshSchedule.objects.update_or_create(
            store_profile=validated_data.get('store_profile'),
            code_article=validated_data.get('code_article'),
            date=validated_data.get('date'),
            defaults=validated_data
        )
        if created:
            logger.info(f"Created new RefreshSchedule instance for store_profile {store_profile.id} and code_article {validated_data.get('code_article')}")
        else:
            logger.info(f"Updated existing RefreshSchedule instance for store_profile {store_profile.id} and code_article {validated_data.get('code_article')}")
        return instance

    def update(self, instance, validated_data):
        store_profile = validated_data.get('store_profile')
        if not isinstance(store_profile, Corak_API_userProfile):
            store_profile = Corak_API_userProfile.objects.get(id=store_profile)
            validated_data['store_profile'] = store_profile

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        logger.info(f"Updated RefreshSchedule instance for store_profile {store_profile.id} and code_article {instance.code_article}")
        return instance

class ProductSerializer(serializers.ModelSerializer):
    custom = CustomSerializer(allow_null=True, required=False)
    promotion = PromotionSerializer(allow_null=True, required=False)
    refresh_schedules = RefreshScheduleSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = Product
        fields = ['code_article', 'custom', 'promotion', 'refresh_schedules', 'store_profile']

    def create(self, validated_data):
        custom_data = validated_data.pop('custom', None)
        promotion_data = validated_data.pop('promotion', None)
        refresh_schedule_data = validated_data.pop('refresh_schedules', [])

        store_profile = validated_data.get('store_profile')
        if not isinstance(store_profile, Corak_API_userProfile):
            store_profile = Corak_API_userProfile.objects.get(id=store_profile)
            validated_data['store_profile'] = store_profile

        custom = None
        if custom_data:
            custom_data['store_profile'] = store_profile.id
            custom_serializer = CustomSerializer(data=custom_data)
            custom_serializer.is_valid(raise_exception=True)
            custom = custom_serializer.save()

        promotion = None
        if promotion_data:
            promotion_data['store_profile'] = store_profile.id
            promotion_serializer = PromotionSerializer(data=promotion_data)
            promotion_serializer.is_valid(raise_exception=True)
            promotion = promotion_serializer.save()

        product, created = Product.objects.update_or_create(
            store_profile=validated_data.get('store_profile'),
            code_article=validated_data.get('code_article'),
            defaults={
                'custom': custom,
                'promotion': promotion,
                **validated_data
            }
        )

        if created:
            logger.info(f"Created new Product instance for store_profile {store_profile.id} and code_article {validated_data.get('code_article')}")
        else:
            logger.info(f"Updated existing Product instance for store_profile {store_profile.id} and code_article {validated_data.get('code_article')}")

        product.refresh_schedules.set([
            RefreshSchedule.objects.get_or_create(
                store_profile=store_profile,
                code_article=validated_data.get('code_article'),
                date=rs_data.get('date')
            )[0] for rs_data in refresh_schedule_data
        ])

        product.save()
        logger.info(f"Product instance with code_article {validated_data.get('code_article')} has been created or updated with refresh schedules.")

        return product

    def update(self, instance, validated_data):
        custom_data = validated_data.pop('custom', None)
        promotion_data = validated_data.pop('promotion', None)
        refresh_schedule_data = validated_data.pop('refresh_schedules', [])

        store_profile = validated_data.get('store_profile')
        if not isinstance(store_profile, Corak_API_userProfile):
            store_profile = Corak_API_userProfile.objects.get(id=store_profile)
            validated_data['store_profile'] = store_profile

        if custom_data:
            custom_data['store_profile'] = store_profile.id
            custom_serializer = CustomSerializer(instance.custom, data=custom_data)
            custom_serializer.is_valid(raise_exception=True)
            custom_serializer.save()

        if promotion_data:
            promotion_data['store_profile'] = store_profile.id
            promotion_serializer = PromotionSerializer(instance.promotion, data=promotion_data)
            promotion_serializer.is_valid(raise_exception=True)
            promotion_serializer.save()

        instance.refresh_schedules.set([
            RefreshSchedule.objects.get_or_create(
                store_profile=store_profile,
                code_article=instance.code_article,
                date=rs_data.get('date')
            )[0] for rs_data in refresh_schedule_data
        ])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        logger.info(f"Updated Product instance for store_profile {store_profile.id} and code_article {instance.code_article} with new data and refresh schedules.")

        return instance
