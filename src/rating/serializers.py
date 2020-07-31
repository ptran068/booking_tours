from rest_framework import serializers
from .models import Rating

class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ('id', 'score', 'user_id', 'tour_id')
        read_only_fields = ('user_id')
