from rest_framework import serializers
from .models import UploadedFile

class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ('file', 'file_type', 'uploaded_at', 'store_profile')
        ref_name = 'CommonUploadedFileSerializer'  # Ajoutez cette ligne
