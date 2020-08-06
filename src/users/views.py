from django.contrib.auth.models import User, auth
from django.views import View
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import AuthCustomTokenSerializer, UserSerializer
import datetime
import jwt
from rest_framework.authtoken.views import ObtainAuthToken
from middlewares.authentication import AuthenticationJWT, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from rest_framework.authentication import authenticate
from payments.services import PaymentService


class Login(ObtainAuthToken):
    serializer_class = AuthCustomTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            data = generate_token(user)
            return data

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateUser(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save()
            instance.set_password(instance.password)
            instance.save()
            try:
                PaymentService.create_customer(user=instance)
            except Exception as e:
                return Response({'error_msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            user = authenticate(email=instance.email, password=request.data['password'])
            data = generate_token(user)
            
            return data
    

def logout(request):
    auth.logout(request)
    return redirect('/')

def generate_token(user):
    payload = {
        'id': str(user.id),
        'email': user.email,
        'phone': user.phone,
        'stripe_id': user.stripe_id,
        'is_superuser': user.is_superuser,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }
    token = jwt.encode(payload, settings.SECRET_KEY)

    payloadRefreshToken = {
        'id': str(user.id),
        'email': user.email,
        'phone': user.phone,
        'stripe_id': user.stripe_id,
        'is_superuser': user.is_superuser,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)
    }
    refreshToken = jwt.encode(payloadRefreshToken, settings.REFRESH_JWT_SECRET)
    user_data = {
        'id': user.id,
        'phone': user.phone,
        'stripe_id': user.stripe_id,
        'email': user.email,
        'is_superuser': user.is_superuser,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)
    }
    return Response({
        'user': user_data,
        'token': token,
        'refreshToken': refreshToken
    })

class Decode_Token(APIView):

    def post(self, request):
        token = request.data['token']
        decode = jwt.decode(token, settings.SECRET_KEY)
        return Response(decode)