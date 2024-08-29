from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status, parsers
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product, Custom, RefreshSchedule, Promotion
from .API_ITEMS_serializers import (
    ProductSerializer, CustomSerializer, PromotionSerializer, RefreshScheduleSerializer
)
from custom_user_management.models import Corak_API_userProfile
import json
import logging

logger = logging.getLogger(__name__)

class StoreProfileAPIViewMixin(object):
    def get_store_profile(self, store_number):
        try:
            return Corak_API_userProfile.objects.get(store_number=store_number)
        except Corak_API_userProfile.DoesNotExist:
            logger.error(f"Store profile with store number {store_number} does not exist.")
            return None

    def get_serializer_context(self):
        context = super().get_serializer_context()
        store_number = self.kwargs.get('store_number')
        store_profile = self.get_store_profile(store_number)
        if store_profile:
            context.update({'store_profile': store_profile, 'store_number': store_number})
        return context

class MultiCreateAPIView(generics.ListCreateAPIView, StoreProfileAPIViewMixin):
    parser_classes = (parsers.JSONParser, parsers.MultiPartParser, parsers.FormParser)

    def post(self, request, *args, **kwargs):
        if getattr(self, 'swagger_fake_view', False):
            return Response()
        
        context = self.get_serializer_context()
        data = self.get_request_data(request)
        if isinstance(data, list):
            responses = [self.process_data(item, context) for item in data]
        else:
            responses = [self.process_data(data, context)]
        return Response(responses, status=status.HTTP_201_CREATED)

    def get_request_data(self, request):
        if 'file' in request.FILES:
            file = request.FILES['file']
            content = file.read().decode('utf-8')
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                logger.error("Erreur de décodage JSON dans le fichier.")
                return Response({"error": "Erreur de décodage JSON dans le fichier"}, status=status.HTTP_400_BAD_REQUEST)
        return request.data

    def process_data(self, item_data, context):
        serializer = self.get_serializer(data=item_data, context=context)
        try:
            serializer.is_valid(raise_exception=True)
            obj = serializer.save()
            return self.get_serializer(obj, context=context).data
        except Exception as e:
            logger.error(f"Erreur lors du traitement des données: {e}")
            return {"error": str(e)}

class ProductListView(MultiCreateAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Product.objects.none()
        
        store_number = self.kwargs.get('store_number')
        store_profile = self.get_store_profile(store_number)
        return Product.objects.filter(store_profile=store_profile) if store_profile else Product.objects.none()

class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView, StoreProfileAPIViewMixin):
    serializer_class = ProductSerializer
    lookup_field = 'code_article'
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Product.objects.none()
        
        store_number = self.kwargs.get('store_number')
        store_profile = self.get_store_profile(store_number)
        return Product.objects.filter(store_profile=store_profile) if store_profile else Product.objects.none()

class CustomListView(MultiCreateAPIView):
    serializer_class = CustomSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Custom.objects.none()
        
        store_number = self.kwargs.get('store_number')
        store_profile = self.get_store_profile(store_number)
        return Custom.objects.filter(store_profile=store_profile) if store_profile else Custom.objects.none()

class CustomRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView, StoreProfileAPIViewMixin):
    serializer_class = CustomSerializer
    lookup_field = 'code_article'
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Custom.objects.none()
        
        store_number = self.kwargs.get('store_number')
        store_profile = self.get_store_profile(store_number)
        return Custom.objects.filter(store_profile=store_profile) if store_profile else Custom.objects.none()

class PromotionListView(MultiCreateAPIView):
    serializer_class = PromotionSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Promotion.objects.none()
        
        store_number = self.kwargs.get('store_number')
        store_profile = self.get_store_profile(store_number)
        return Promotion.objects.filter(store_profile=store_profile) if store_profile else Promotion.objects.none()

class PromotionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView, StoreProfileAPIViewMixin):
    serializer_class = PromotionSerializer
    lookup_field = 'code_article'
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Promotion.objects.none()
        
        store_number = self.kwargs.get('store_number')
        store_profile = self.get_store_profile(store_number)
        return Promotion.objects.filter(store_profile=store_profile) if store_profile else Promotion.objects.none()

class RefreshScheduleListView(MultiCreateAPIView):
    serializer_class = RefreshScheduleSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return RefreshSchedule.objects.none()
        
        store_number = self.kwargs.get('store_number')
        store_profile = self.get_store_profile(store_number)
        return RefreshSchedule.objects.filter(store_profile=store_profile) if store_profile else RefreshSchedule.objects.none()

    def perform_create(self, serializer):
        store_number = self.kwargs.get('store_number')
        store_profile = self.get_store_profile(store_number)
        serializer.save(store_profile=store_profile)

class RefreshScheduleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView, StoreProfileAPIViewMixin):
    serializer_class = RefreshScheduleSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return RefreshSchedule.objects.none()
        
        store_number = self.kwargs.get('store_number')
        store_profile = self.get_store_profile(store_number)
        return RefreshSchedule.objects.filter(store_profile=store_profile) if store_profile else RefreshSchedule.objects.none()

class PromoDataUploadView(APIView):
    parser_classes = (parsers.JSONParser, parsers.MultiPartParser, parsers.FormParser)
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if getattr(self, 'swagger_fake_view', False):
            return Response()
        
        data_list = self.get_request_data(request)
        context = self.get_serializer_context()

        if isinstance(data_list, list):
            responses = [self.process_data(item, context) for item in data_list]
        else:
            responses = [self.process_data(data_list, context)]

        return Response(responses, status=status.HTTP_201_CREATED)

    def get_request_data(self, request):
        if 'file' in request.FILES:
            file = request.FILES['file']
            content = file.read().decode('utf-8')
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                logger.error("Erreur de décodage JSON dans le fichier.")
                return Response({"error": "Erreur de décodage JSON dans le fichier"}, status=status.HTTP_400_BAD_REQUEST)
        return request.data

    def process_data(self, item_data, context):
        custom_data = item_data.get('custom', {})
        promotion_data = item_data.get('promotion', {})
        refresh_schedules_data = item_data.get('refreshSchedules', [])
        code_article = item_data.get('id')

        store_profile = context['store_profile']

        # Enregistrer Custom
        custom_data['code_article'] = code_article
        custom_data['store_profile'] = store_profile.id
        custom_serializer = CustomSerializer(data=custom_data, context=context)
        if custom_serializer.is_valid():
            custom_instance = custom_serializer.save()
        else:
            logger.error(f"Erreur lors de la validation de CustomSerializer: {custom_serializer.errors}")
            return {"error": custom_serializer.errors}

        # Enregistrer Promotion
        promotion_data['code_article'] = code_article
        promotion_data['store_profile'] = store_profile.id
        promotion_serializer = PromotionSerializer(data=promotion_data, context=context)
        if promotion_serializer.is_valid():
            promotion_instance = promotion_serializer.save()
        else:
            logger.error(f"Erreur lors de la validation de PromotionSerializer: {promotion_serializer.errors}")
            return {"error": promotion_serializer.errors}

        # Enregistrer RefreshSchedule
        refresh_schedule_responses = []
        for rs_data in refresh_schedules_data:
            rs_data['code_article'] = code_article
            rs_data['store_profile'] = store_profile.id
            rs_serializer = RefreshScheduleSerializer(data=rs_data, context=context)
            if rs_serializer.is_valid():
                rs_instance = rs_serializer.save()
                refresh_schedule_responses.append(rs_serializer.data)
            else:
                logger.error(f"Erreur lors de la validation de RefreshScheduleSerializer: {rs_serializer.errors}")
                refresh_schedule_responses.append({"error": rs_serializer.errors})

        # Récupérer ou créer le produit associé
        product, created = Product.objects.get_or_create(
            code_article=code_article,
            store_profile=store_profile
        )
        product.custom = custom_instance
        product.promotion = promotion_instance
        product.refresh_schedules.set([rs_instance for rs_instance in refresh_schedule_responses if 'id' in rs_instance])
        product.save()

        return {
            "custom": CustomSerializer(custom_instance, context=context).data,
            "promotion": PromotionSerializer(promotion_instance, context=context).data,
            "refreshSchedules": refresh_schedule_responses,
            "product": ProductSerializer(product, context=context).data
        }
