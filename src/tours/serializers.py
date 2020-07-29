from rest_framework import serializers
from .models import Categories, Tours

class CategoriSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = '__all__'

class ToursSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tours
        fields = '__all__'
