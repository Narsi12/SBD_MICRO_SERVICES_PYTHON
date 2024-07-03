import uuid
import logging
from rest_framework import serializers
from .models import User, RoleLkp
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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','name', 'email','role_id', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            name = validated_data['name'],
            email=validated_data['email'],
            role_id = validated_data['role_id'],
            password=validated_data['password']
        )
        logger.info(f"{user.name} Registered Successfully")
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        logger.info(f"User {instance.user_name} updated successfully.")
        return instance

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

class RoleSerializer(BaseModelSerializer):

    class Meta:
        model = RoleLkp
        fields = ['id', 'role', 'description', 'created_by', 'created_by_date', 'updated_by', 'updated_by_date']
