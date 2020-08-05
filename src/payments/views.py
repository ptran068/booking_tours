from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from middlewares.authentication import AuthenticationJWT
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomerSerializer, PaymentMethodSerializer, PaymentIntentSerializer, PaymentSerializer
from .services import PaymentService
from tours.models import Tours
from .models import Payments
from rest_framework import filters
from django.conf import settings
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from rest_framework.generics import ListAPIView
from middlewares.pagination import CustomPagination


class Customer(APIView):

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                customer = serializer.create(user=request.user)
                data = {
                    "email": customer.email,
                    'name': customer.name,
                    'phone': customer.phone,
                    'description': customer.description,
                    'currency': customer.currency,
                    'balance': customer.balance,
                    'created': customer.created
                }
                return Response(data=data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error_msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PaymentMethod(APIView):

    def get(self, request):
        try:
            list_payment_method = PaymentService.get_list_payments_method_custommer(user=request.user)
            context= []
            for item in list_payment_method.data:
                data = {
                    'id': item.id,
                    'brand': item.card.brand,
                    'country': item.card.country,
                    'expired_month': item.card.exp_month,
                    'expired_year': item.card.exp_year,
                    'last4': item.card.last4,
                    'created': item.created
                }
                context.append(data)

            return Response(data=context, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error_msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = PaymentMethodSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                payment_method = serializer.create(user=request.user)
                data = {
                    'id': payment_method.id,
                    'brand': payment_method.card.brand,
                    'country': payment_method.card.country,
                    'expired_month': payment_method.card.exp_month,
                    'expired_year': payment_method.card.exp_year,
                    'last4': payment_method.card.last4,
                    'created': payment_method.created
                }
                return Response(data=data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error_msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PaymentIntent(APIView):

    def post(self, request):
        tour_id = request.query_params.get('tour_id')
        tour = Tours.objects.filter(id=tour_id).first()
        serializer = PaymentIntentSerializer(data=request.data)
        if tour is None:
            return Response({'error_msg': 'Tour not found'}, status=status.HTTP_404_NOT_FOUND)
        if serializer.is_valid(raise_exception=True):
            try:
                payment_intent = serializer.create(stripe_id=request.user.stripe_id, amount=tour.amount)
                payment = Payments.objects.create(
                    author = request.user,
                    payment_intent_id = payment_intent.id,
                    amount = payment_intent.amount,
                    tour = tour,
                    card_id = payment_intent.payment_method,
                    description = payment_intent.description,
                    status = 'PENDING'
                )
                context = {
                    'payment_id': payment.id,
                    'payment_intent_id': payment_intent.id,
                    'card_id': payment_intent.payment_method,
                    'description': payment_intent.description,
                    'amount': payment_intent.amount,
                    'created': payment_intent.created,
                    'status': payment_intent.status,
                }
                return Response(data=context, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error_msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ConfirmPaymentIntent(APIView):

    def post(self, request):
        payment_id = request.query_params.get('payment_id')
        payment = Payments.objects.get_payment_by_id(id=payment_id)
        if payment is None:
            return Response({'error_msg': 'payment not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            payment_intent = PaymentService.confirm_payment_intent(payment_intent_id=payment.payment_intent_id)
            payment.status = 'PAID'
            payment.save()
            context = {
                'id': payment_intent.id,
                'amount': payment_intent.amount,
                'amount_received': payment_intent.amount_received,
                'created': payment_intent.created,
                'description': payment_intent.description,
                'status': payment_intent.status,
                'currency': payment_intent.currency,
                'customer': payment_intent.customer
            }
            return Response(data=context, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error_msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CancelPaymentIntent(APIView):

    def post(self, request):
        payment_id = request.query_params.get('payment_id')
        payment = Payments.objects.get_payment_by_id(id=payment_id)
        if payment is None:
            return Response({'error_msg': 'payment not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            payment_intent = PaymentService.cancel_payment_intent(payment_intent_id=payment.payment_intent_id)
            payment.delete()
            return Response(data= {'msg': 'Delete successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error_msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RetrievePaymentIntent(APIView):    
    def get(self, request):
        payment_id = request.query_params.get('payment_id')
        payment = Payments.objects.get_payment_by_id(id=payment_id)
        if payment is None:
            return Response({'error_msg': 'payment not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            payment_intent = PaymentService.retrieve_payment_intent(payment_intent_id=payment.payment_intent_id)
            context = {
                'id': payment_intent.id,
                'amount': payment_intent.amount,
                'created': payment_intent.created,
                'description': payment_intent.description,
                'status': payment_intent.status,
                'currency': payment_intent.currency,
                'customer': payment_intent.customer
            }
            return Response(data=context, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error_msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PaymentsList(APIView):
    def get(self, request):
        payments = Payments.objects.all().order_by('-created_at')
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(payments, request)
        pserializer=PaymentSerializer(result_page,many=True)
        return paginator.get_paginated_response(pserializer.data)

