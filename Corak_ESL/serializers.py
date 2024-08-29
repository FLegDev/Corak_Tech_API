# serializers.py dans votre application Django

from rest_framework import serializers
from .models import Export2Zkong

class Export2ZkongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Export2Zkong
        fields = '__all__'  # Ou spécifiez les champs que vous voulez inclure
