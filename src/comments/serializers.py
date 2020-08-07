from .models import Comment
from rest_framework import serializers
from users.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField('get_user')

    def get_user(self, obj):
        return {'id': obj.created_by.id, 'email': obj.created_by.email,
                'first_name': obj.created_by.first_name,
                'last_name': obj.created_by.last_name}

    class Meta:
        model = Comment
        fields = '__all__'
