from rest_framework import serializers
from .models import Book
from django.utils import timezone


class BookingSerializer(serializers.ModelSerializer):
    tours = serializers.SerializerMethodField("get_tour")

    def get_tour(self, obj):
        return {'id': obj.tours.id, 'description': obj.tours.description,
                'address': obj.tours.address, 'amount': obj.tours.amount,
                'duration': obj.tours.duration, 'quantity_members': obj.tours.quantity_members,
                'policy': obj.tours.policy}

    class Meta:
        model = Book
        fields = '__all__'

    def validate_start_date(self, value):
        if value <= timezone.now().date():
            raise serializers.ValidationError('The start date is wrong')
        return value
