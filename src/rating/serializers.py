from rest_framework import serializers
from .models import Rating

class RatingSerializer(serializers.ModelSerializer):
    tour_id = serializers.SerializerMethodField("get_tour")

    def get_tour(self, obj):
        return {'id': obj.tour_id.id}

    class Meta:
        model = Rating
        fields = ('id', 'score', 'user_id', 'tour_id')
        read_only_fields = ['user_id', 'tour_id']
