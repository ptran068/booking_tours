from rest_framework import serializers
from .models import Book
from users.serializers import UserSerializer
from tours.serializers import ToursSerializer


class BookingSerializer(serializers.ModelSerializer):
    tours = serializers.SerializerMethodField("get_tour")

    def get_tour(self, obj):
        return {'id': obj.tours.id, 'description': obj.tours.description,
                'address': obj.tours.address, 'amount': obj.tours.price,
                'duration': obj.tours.duration, 'quantity_members': obj.tours.quantity_members,
                'policy': obj.tours.policy}

    class Meta:
        model = Book
        fields = '__all__'
