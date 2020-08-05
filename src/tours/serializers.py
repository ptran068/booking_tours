from rest_framework import serializers
from .models import Tours
from files.models import File
from users.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name']

class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = '__all__'

class ToursSerializer(serializers.ModelSerializer):
    images = FileSerializer(many=True)
    created_by = CustomUserSerializer(many=False)

    class Meta:
        model = Tours
        fields = '__all__'
