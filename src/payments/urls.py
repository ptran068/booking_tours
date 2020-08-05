from django.urls import path
from .views import  Customer, CancelPaymentIntent, PaymentMethod, PaymentIntent, PaymentsList, RetrievePaymentIntent, ConfirmPaymentIntent
from . import  views

urlpatterns = [
    path('customer', Customer.as_view()),
    path('', PaymentsList.as_view()),
    path('payment-method', PaymentMethod.as_view()),
    path('payment-intent', PaymentIntent.as_view()),
    path('payment-intent/retrieve', RetrievePaymentIntent.as_view()),
    path('payment-intent/confirm', ConfirmPaymentIntent.as_view()),
    path('payment-intent/cancel', CancelPaymentIntent.as_view()),
]

