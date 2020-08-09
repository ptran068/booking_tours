from rest_framework import serializers
from .models import Review
from files.serializers import FileSerializer


class ReviewSerializer(serializers.ModelSerializer):
    images = FileSerializer(many=True, read_only=True)
    created_by = serializers.SerializerMethodField('get_user')

    def get_user(self, obj):
        return {'first_name': obj.created_by.first_name, 'last_name': obj.created_by.last_name,
                'email': obj.created_by.email, }

    class Meta:
        model = Review
        fields = '__all__'
