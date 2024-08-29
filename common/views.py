import json
import os
import logging
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .models import UploadedFile
from custom_user_management.models import Corak_API_userProfile
from .serializers import UploadedFileSerializer
from common.authentication import CustomTokenAuthentication
from common.response_utils import (
    response_201, response_400, response_401, response_402, response_403, response_404, response_500, response_503
)
from common.service_checks import check_service_availability

logger = logging.getLogger('common')

class FileUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, store_number, *args, **kwargs):
        if getattr(self, 'swagger_fake_view', False):
            return Response()

        logger.info(f"Received request with method {request.method}")
        logger.info(f"Request headers: {request.headers}")
        logger.info(f"Request data: {request.data}")
        logger.info(f"Request files: {request.FILES}")

        try:
            store_profile = get_object_or_404(Corak_API_userProfile, store_number=store_number)
            logger.info(f"Store profile found: {store_profile}")
        except Corak_API_userProfile.DoesNotExist:
            logger.error(f"Store profile not found for store number: {store_number}")
            return response_404(request, "Store profile not found")

        unavailable_service = check_service_availability()
        if unavailable_service:
            logger.error(f"Service unavailable: {unavailable_service}")
            return response_503(request, unavailable_service)

        if isinstance(request.data, (list, dict)):
            data = request.data if isinstance(request.data, list) else [request.data]
            for item in data:
                item['store_profile'] = store_profile.id

            file_type = UploadedFile().determine_file_type(data=data)
            logger.info(f"Determined file type: {file_type}")

            file_name = f"{file_type}_{store_profile.store_number}_{timezone.now().strftime('%Y%m%d%H%M%S')}.json"
            file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', file_type, file_name)  # Utiliser des chemins relatifs

            logger.debug(f"Creating directory: {os.path.dirname(file_path)}")
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            logger.debug(f"Saving data to file: {file_path}")
            try:
                with open(file_path, 'w') as json_file:
                    json.dump(data, json_file)
                logger.info(f"Data saved to file: {file_path}")

                uploaded_file = UploadedFile.objects.create(store_profile=store_profile, file_type=file_type, file=os.path.relpath(file_path, settings.MEDIA_ROOT))
                logger.info(f"UploadedFile created with ID: {uploaded_file.id} and file path: {uploaded_file.file}")

                # Répondre immédiatement au client avant tout traitement supplémentaire
                response_data = {
                    "file_type": file_type,
                    "file_path": uploaded_file.file.url,
                    "message": "File uploaded successfully"
                }

                logger.info(f"Response data: {response_data}")
                response = Response(response_data, status=status.HTTP_201_CREATED)

                # Ajoutez ici tout traitement supplémentaire que vous devez effectuer après avoir répondu au client
                # ...

                return response
            except Exception as e:
                logger.error(f"Error writing to file {file_path}: {e}")
                return response_500(request, f"Error writing to file {file_path}: {e}")

        else:
            logger.error("No valid JSON data provided")
            return response_400(request, "No valid JSON data provided")
