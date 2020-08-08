from rest_framework import serializers
from rest_framework import exceptions
from rest_framework.authentication import authenticate
from .services import PaymentService
from .models import Payments
from tours.models import Tours


class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tours
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    tour = TourSerializer(many=False)

    class Meta:
        model = Payments
        fields = '__all__'


class PaymentMethodSerializer(serializers.Serializer):
    number = serializers.CharField(max_length = 255)
    expired_month = serializers.IntegerField()
    expired_year = serializers.IntegerField()
    cvc = serializers.IntegerField()

    def create(self, user):
        return PaymentService.create_payment_method(user=user, data=self.validated_data)


class PaymentIntentSerializer(serializers.Serializer):
    payment_method_id = serializers.CharField(max_length = 255)
    description = serializers.CharField(max_length = 255, required=False)

    def create(self, stripe_id, amount):
        return PaymentService.create_payment_intent(stripe_id=stripe_id, amount=amount, data=self.validated_data)

