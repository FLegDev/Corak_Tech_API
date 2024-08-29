from rest_framework import serializers
from .models import UploadedFile, ParsedData

class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ('file', 'uploaded_at', 'store_profile')

class ParsedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParsedData
        fields = '__all__'
