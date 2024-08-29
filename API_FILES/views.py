import logging
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import UploadedFile
from custom_user_management.models import Corak_API_userProfile
from .API_FILE_serializers import UploadedFileSerializer
from common.authentication import CustomTokenAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .tasks import parse_uploaded_file  # Import de la tâche Celery

logger = logging.getLogger('api_files')  # Correct logging declaration

class FileUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Upload a file related to EEG data for a specific store",
        tags=['FluxAPI_FILES'],
        manual_parameters=[
            openapi.Parameter(
                name='file',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                description='EEG file to upload',
                required=True,
            ),
            openapi.Parameter(
                name='store_number',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                description='Store number',
                required=True,
            ),
        ],
        responses={
            201: openapi.Response('File uploaded successfully', UploadedFileSerializer),
            400: 'Bad Request',
            404: 'Store profile not found',
            500: 'Internal Server Error'
        }
    )
    def post(self, request, store_number, *args, **kwargs):
        if getattr(self, 'swagger_fake_view', False):
            return Response()

        logger.info(f"Received POST request for store_number: {store_number}")
        
        try:
            # Récupération du profil du magasin en fonction du store_number
            store_profile = get_object_or_404(Corak_API_userProfile, store_number=store_number)
            logger.info(f"Store profile found for store_number: {store_number}")

            # Vérification de la présence d'un fichier dans la requête
            if not request.FILES:
                logger.error("No file provided in the request")
                return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

            # Extraction du premier fichier depuis la requête (peu importe la clé)
            file_obj = next(iter(request.FILES.values()))
            logger.info(f"Processing file: {file_obj.name}")

            # Création du dictionnaire de données à passer au serializer
            data = {
                'file': file_obj,
                'store_profile': store_profile.id,
            }
            logger.debug(f"Data to serialize: {data}")

            # Gestion du téléchargement du fichier
            file_serializer = UploadedFileSerializer(data=data)
            if file_serializer.is_valid():
                uploaded_file_instance = file_serializer.save()
                logger.info(f"File {file_obj.name} uploaded successfully for store {store_number}")

                # Répondre immédiatement au client avant le traitement en arrière-plan
                response_data = file_serializer.data
                response_data.update({"message": "File uploaded successfully. Processing started."})
                response_status = status.HTTP_201_CREATED

                # Appel de la tâche Celery pour traiter le fichier
                parse_uploaded_file.delay(uploaded_file_instance.id)
                logger.info(f"Background processing started for file {file_obj.name}")

                return Response(response_data, status=response_status)
            else:
                # Récupération du premier message d'erreur du dictionnaire d'erreurs
                error_message = next(iter(file_serializer.errors.values()))[0]
                logger.error(f"File upload failed: {error_message}")
                return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

        except Corak_API_userProfile.DoesNotExist:
            logger.error(f"Store profile with store number {store_number} does not exist")
            return Response({"error": "Store profile not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}", exc_info=True)
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
