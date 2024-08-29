import logging
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import Certificates, CustomDetail, Product, Fresh
from custom_user_management.models import Corak_API_userProfile

# Configuration du logger pour l'application ardoise
logger = logging.getLogger('ardoise')

class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificates
        fields = ['fairTrade', 'organic', 'environmentallyFriendly', 'code_article']

class CustomDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomDetail
        fields = [
            'libelle_cr_auto', 'libelle_lg_auto', 'geeti1_auto', 'type_auto',
            'traitement_auto', 'conditionnement_auto', 'code_article'
        ]
        ref_name = 'ArdoiseCustomDetailSerializer'  # Ajoutez cette ligne

class ProductSerializer(serializers.ModelSerializer):
    custom = CustomDetailSerializer()
    certificates = CertificateSerializer()
    id = serializers.CharField(source='code_article', required=True)

    class Meta:
        model = Product
        fields = ['id', 'custom', 'price', 'capacity', 'unitPriceUnit', 'currency', 'certificates']
        ref_name = 'ArdoiseItemProduct'  # Correction : inclure ref_name ici

    def create(self, validated_data):
        logger.info("Creating new product with data: %s", validated_data)
        custom_data = validated_data.pop('custom', {})
        certificates_data = validated_data.pop('certificates', {})

        store_profile = self.context['store_profile']
        code_article = validated_data.pop('code_article')

        try:
            custom_instance, _ = CustomDetail.objects.update_or_create(
                code_article=code_article, store_profile=store_profile, defaults=custom_data
            )

            certificates_instance, _ = Certificates.objects.update_or_create(
                code_article=code_article, store_profile=store_profile, defaults=certificates_data
            )

            product_instance, _ = Product.objects.update_or_create(
                code_article=code_article, store_profile=store_profile,
                defaults={'custom': custom_instance, 'certificates': certificates_instance, **validated_data}
            )
            logger.info("Product created successfully: %s", product_instance)
            return product_instance

        except Exception as e:
            logger.error("Error creating product: %s", e)
            raise serializers.ValidationError("An error occurred while creating the product")

    def to_representation(self, instance):
        representation = super(ProductSerializer, self).to_representation(instance)
        logger.debug("Product representation: %s", representation)
        return representation

class CustomDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomDetail
        fields = '__all__'

    def create(self, validated_data):
        logger.info("Creating or updating CustomDetail with data: %s", validated_data)
        try:
            store_profile = validated_data.get('store_profile')
            if not isinstance(store_profile, Corak_API_userProfile):
                store_profile = Corak_API_userProfile.objects.get(id=store_profile)
                validated_data['store_profile'] = store_profile

            instance, created = CustomDetail.objects.update_or_create(
                store_profile=validated_data.get('store_profile'),
                code_article=validated_data.get('code_article'),
                defaults=validated_data
            )
            logger.info("CustomDetail %s successfully", "created" if created else "updated")
            return instance

        except Exception as e:
            logger.error("Error creating or updating CustomDetail: %s", e)
            raise serializers.ValidationError("An error occurred while creating or updating CustomDetail")

    def update(self, instance, validated_data):
        logger.info("Updating CustomDetail with data: %s", validated_data)
        try:
            store_profile = validated_data.get('store_profile')
            if not isinstance(store_profile, Corak_API_userProfile):
                store_profile = Corak_API_userProfile.objects.get(id=store_profile)
                validated_data['store_profile'] = store_profile

            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            logger.info("CustomDetail updated successfully")
            return instance

        except Exception as e:
            logger.error("Error updating CustomDetail: %s", e)
            raise serializers.ValidationError("An error occurred while updating CustomDetail")

class CertificateDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificates
        fields = '__all__'

    def create(self, validated_data):
        logger.info("Creating or updating Certificates with data: %s", validated_data)
        try:
            store_profile = validated_data.get('store_profile')
            if not isinstance(store_profile, Corak_API_userProfile):
                store_profile = Corak_API_userProfile.objects.get(id=store_profile)
                validated_data['store_profile'] = store_profile

            instance, created = Certificates.objects.update_or_create(
                store_profile=validated_data.get('store_profile'),
                code_article=validated_data.get('code_article'),
                defaults=validated_data
            )
            logger.info("Certificates %s successfully", "created" if created else "updated")
            return instance

        except Exception as e:
            logger.error("Error creating or updating Certificates: %s", e)
            raise serializers.ValidationError("An error occurred while creating or updating Certificates")

    def update(self, instance, validated_data):
        logger.info("Updating Certificates with data: %s", validated_data)
        try:
            store_profile = validated_data.get('store_profile')
            if not isinstance(store_profile, Corak_API_userProfile):
                store_profile = Corak_API_userProfile.objects.get(id=store_profile)
                validated_data['store_profile'] = store_profile

            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            logger.info("Certificates updated successfully")
            return instance

        except Exception as e:
            logger.error("Error updating Certificates: %s", e)
            raise serializers.ValidationError("An error occurred while updating Certificates")

class FreshSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fresh
        fields = '__all__'

    def create(self, validated_data):
        logger.info("Creating or updating Fresh with data: %s", validated_data)
        try:
            store_profile = validated_data.get('store_profile')
            if not isinstance(store_profile, Corak_API_userProfile):
                store_profile = Corak_API_userProfile.objects.get(id=store_profile)
                validated_data['store_profile'] = store_profile

            instance, created = Fresh.objects.update_or_create(
                store_profile=validated_data.get('store_profile'),
                code_article=validated_data.get('code_article'),
                defaults=validated_data
            )
            logger.info("Fresh %s successfully", "created" if created else "updated")
            return instance

        except Exception as e:
            logger.error("Error creating or updating Fresh: %s", e)
            raise serializers.ValidationError("An error occurred while creating or updating Fresh")

    def update(self, instance, validated_data):
        logger.info("Updating Fresh with data: %s", validated_data)
        try:
            store_profile = validated_data.get('store_profile')
            if not isinstance(store_profile, Corak_API_userProfile):
                store_profile = Corak_API_userProfile.objects.get(id=store_profile)
                validated_data['store_profile'] = store_profile

            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            logger.info("Fresh updated successfully")
            return instance

        except Exception as e:
            logger.error("Error updating Fresh: %s", e)
            raise serializers.ValidationError("An error occurred while updating Fresh")
