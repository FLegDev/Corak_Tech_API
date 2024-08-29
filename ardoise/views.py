import logging
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status, parsers
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from custom_user_management.models import Corak_API_userProfile
from .models import Certificates, CustomDetail, Product
from .ardoise_serializers import CertificateSerializer, CustomDetailSerializer, ProductSerializer
from drf_yasg.utils import swagger_auto_schema

import json

logger = logging.getLogger('common')

class MultiCreateAPIView(generics.ListCreateAPIView):
    parser_classes = (parsers.JSONParser, parsers.MultiPartParser, parsers.FormParser)

    def post(self, request, *args, **kwargs):
        if 'file' in request.FILES:
            file = request.FILES['file']
            content = file.read().decode('utf-8')
            try:
                data = json.loads(content)
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {e}")
                return Response({"error": "Erreur de décodage JSON dans le fichier"},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            data = request.data

        if isinstance(data, list):
            created_objects = []
            for item_data in data:
                serializer = self.get_serializer(data=item_data)
                if serializer.is_valid():
                    obj = serializer.save()
                    created_objects.append(obj)
                else:
                    logger.error(f"Validation error: {serializer.errors}")
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response([self.get_serializer(obj).data for obj in created_objects], status=status.HTTP_201_CREATED)
        else:
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                obj = serializer.save()
                return Response(self.get_serializer(obj).data, status=status.HTTP_201_CREATED)
            else:
                logger.error(f"Validation error: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: ProductSerializer(many=True)})
    def get(self, request, store_number, *args, **kwargs):
        if getattr(self, 'swagger_fake_view', False):
            logger.info("Swagger fake view detected")
            return Response()
        try:
            store_profile = get_object_or_404(Corak_API_userProfile, store_number=store_number)
            products = Product.objects.filter(store_profile=store_profile)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error in ProductListView GET: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(request_body=ProductSerializer)
    def post(self, request, store_number, format=None):
        try:
            store_profile = get_object_or_404(Corak_API_userProfile, store_number=store_number)
            data = request.data
            if isinstance(data, list):
                responses = []
                for item in data:
                    item_serializer = ProductSerializer(data=item, context={'request': request, 'store_profile': store_profile})
                    if item_serializer.is_valid():
                        item_serializer.save()
                        responses.append(item_serializer.data)
                    else:
                        logger.error(f"Validation error: {item_serializer.errors}")
                        return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response(responses, status=status.HTTP_201_CREATED)
            else:
                serializer = ProductSerializer(data=data, context={'request': request, 'store_profile': store_profile})
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    logger.error(f"Validation error: {serializer.errors}")
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error in ProductListView POST: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            logger.info("Swagger fake view detected")
            return Product.objects.none()
        try:
            store_number = self.kwargs['store_number']
            store_profile = get_object_or_404(Corak_API_userProfile, store_number=store_number)
            return Product.objects.filter(store_profile=store_profile)
        except Exception as e:
            logger.error(f"Error in ProductRetrieveUpdateDestroyView: {e}")
            return Product.objects.none()

class CustomDetailListCreateView(generics.ListCreateAPIView):
    serializer_class = CustomDetailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            logger.info("Swagger fake view detected")
            return CustomDetail.objects.none()
        try:
            store_number = self.kwargs['store_number']
            store_profile = get_object_or_404(Corak_API_userProfile, store_number=store_number)
            return CustomDetail.objects.filter(store_profile=store_profile)
        except Exception as e:
            logger.error(f"Error in CustomDetailListCreateView: {e}")
            return CustomDetail.objects.none()

    def perform_create(self, serializer):
        try:
            store_number = self.kwargs['store_number']
            store_profile = get_object_or_404(Corak_API_userProfile, store_number=store_number)
            serializer.save(store_profile=store_profile)
        except Exception as e:
            logger.error(f"Error in CustomDetailListCreateView perform_create: {e}")

class CustomDetailDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CustomDetailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            logger.info("Swagger fake view detected")
            return CustomDetail.objects.none()
        try:
            store_number = self.kwargs['store_number']
            store_profile = get_object_or_404(Corak_API_userProfile, store_number=store_number)
            return CustomDetail.objects.filter(store_profile=store_profile)
        except Exception as e:
            logger.error(f"Error in CustomDetailDetailView: {e}")
            return CustomDetail.objects.none()

class CertificateListCreateView(generics.ListCreateAPIView):
    serializer_class = CertificateSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            logger.info("Swagger fake view detected")
            return Certificates.objects.none()
        try:
            store_number = self.kwargs['store_number']
            store_profile = get_object_or_404(Corak_API_userProfile, store_number=store_number)
            return Certificates.objects.filter(store_profile=store_profile)
        except Exception as e:
            logger.error(f"Error in CertificateListCreateView: {e}")
            return Certificates.objects.none()

    def perform_create(self, serializer):
        try:
            store_number = self.kwargs['store_number']
            store_profile = get_object_or_404(Corak_API_userProfile, store_number=store_number)
            serializer.save(store_profile=store_profile)
        except Exception as e:
            logger.error(f"Error in CertificateListCreateView perform_create: {e}")

class CertificateDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CertificateSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            logger.info("Swagger fake view detected")
            return Certificates.objects.none()
        try:
            store_number = self.kwargs['store_number']
            store_profile = get_object_or_404(Corak_API_userProfile, store_number=store_number)
            return Certificates.objects.filter(store_profile=store_profile)
        except Exception as e:
            logger.error(f"Error in CertificateDetailView: {e}")
            return Certificates.objects.none()
