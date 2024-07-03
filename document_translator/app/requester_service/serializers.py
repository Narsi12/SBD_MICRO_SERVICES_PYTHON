import uuid
import logging
from rest_framework import serializers
from .models import LanguageLkp
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

logger = logging.getLogger(__name__)

class BaseModelSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if isinstance(representation['created_by'], uuid.UUID):
            representation['created_by'] = str(representation['created_by'])
        if representation['updated_by'] and isinstance(representation['updated_by'], uuid.UUID):
            representation['updated_by'] = str(representation['updated_by'])
        return representation

class LanguageSerializer(BaseModelSerializer):
    class Meta:
        model = LanguageLkp
        fields = ['id', 'language', 'language_abbreviation', 'created_by', 'created_by_date', 'updated_by', 'updated_by_date']
