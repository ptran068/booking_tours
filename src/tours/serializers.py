from files.models import File
from rest_framework import serializers
from users.models import CustomUser
from .models import Tours

class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name']

class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = '__all__'

class ToursSerializer(serializers.ModelSerializer):
    images = FileSerializer(many=True, read_only=True)
    created_by = CustomUserSerializer(many=False, read_only=True)

    class Meta:
        model = Tours
        fields = ['id', 'images', 'created_by', 'title',
                  'description', 'views', 'address', 'amount',
                  'duration', 'quantity_members', 'policy',
                  'category', 'video_id', 'avg_rating']
