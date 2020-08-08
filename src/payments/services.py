from django.conf import settings
import stripe
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from rest_framework.response import Response


class PaymentService:
    stripe.api_key = settings.STRIPE_SECRET_KEY
    User = get_user_model()

    @classmethod
    def create_customer(cls, user):
        if user.stripe_id is not None:
            raise Exception('stripe_id already exists')        
        customer = stripe.Customer.create(
            email=user.email,
            name=str(user.first_name + ' ' + user.last_name),
            phone=user.phone,
        )
        if customer is None:
            raise Exception('Create customer wrongs')
        user.stripe_id = customer.stripe_id
        user.save()
        return customer

    @classmethod
    def create_payment_method(cls, user, data):
        if user.stripe_id is None:
            raise Exception('stripe_id not found')
        payment_method = stripe.PaymentMethod.create(
            type = 'card',
            card = {
                'number': data.get('number'),
                'exp_month': data.get('expired_month'),
                'exp_year': data.get('expired_year'),
                'cvc': data.get('cvc'),
            },
        )
        if payment_method is None:
            raise Exception('Create payment method errror')        
        attach_to_customer = stripe.PaymentMethod.attach(
            payment_method.id,
            customer=user.stripe_id,
        )
        if attach_to_customer is None:
            raise Exception('Attach payment method to customer wrongs')            
        return payment_method

    @classmethod
    def get_list_payments_method_custommer(cls, user):
        if user.stripe_id is None:
            raise Exception('stripe_id not found')

        list_payments_method = stripe.PaymentMethod.list(
            customer=user.stripe_id,
            type='card',
        )

        if list_payments_method is None:
            raise Exception('Not found list payments method')

        return list_payments_method

    @classmethod
    def create_payment_intent(cls, stripe_id, amount, data):
        if amount is None:
            raise Exception('amount not found')
        payment_intent = stripe.PaymentIntent.create(
            amount = amount,
            currency = 'usd',
            payment_method_types = ['card'],
            customer = stripe_id,
            payment_method = data.get('payment_method_id'),
            description = data.get('description')
        )
        if payment_intent is None:
            raise Exception('create payment intent wrongs')

        return payment_intent

    @classmethod
    def confirm_payment_intent(cls, payment_intent_id):
        if payment_intent_id is None:
            raise Exception('payment_intent_id not found')
        confirm_payment_intent = stripe.PaymentIntent.confirm(
            payment_intent_id,
        )
        if confirm_payment_intent is None:
            raise Exception('confrim payment intent wrongs')

        return confirm_payment_intent

    @classmethod
    def cancel_payment_intent(cls, payment_intent_id):
        if payment_intent_id is None:
            raise Exception('payment_intent_id not found')
        cancel_payment_intent = stripe.PaymentIntent.cancel(
            payment_intent_id,
        )
        if cancel_payment_intent is None:
            raise Exception('cancel payment intent wrongs')

        return cancel_payment_intent

    @classmethod
    def retrieve_payment_intent(cls, payment_intent_id):
        if payment_intent_id is None:
            raise Exception('payment_intent_id not found')
        cancel_payment_intent = stripe.PaymentIntent.retrieve(
            payment_intent_id,
        )
        if cancel_payment_intent is None:
            raise Exception('retrieve payment intent wrongs')

        return cancel_payment_intent

    @classmethod
    def create_charge(cls, data):
        if data is None:
            raise Exception('data not found')
        charge = stripe.Charge.create(
            amount=data.get('amount'),
            currency='usd',
            source=data.get('token'),
            description=data.get('description')
        )
        if charge is None:
            raise Exception('retrieve payment intent wrongs')

        return charge
    

