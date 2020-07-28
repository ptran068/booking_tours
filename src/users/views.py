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

class Login(ObtainAuthToken):
    serializer_class = AuthCustomTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            payload = {
                'email': user.email,
                'is_superuser': user.is_superuser,
                'iat': datetime.datetime.utcnow(),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
            }
            token = jwt.encode(payload, settings.SECRET_KEY)

            payloadRefreshToken = {
                'email': user.email,
                'is_superuser': user.is_superuser,
                'iat': datetime.datetime.utcnow(),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)
            }
            refreshToken = jwt.encode(payloadRefreshToken, settings.REFRESH_JWT_SECRET)

            return Response({
                'token': token,
                'refreshToken': refreshToken
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateUser(CreateAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()

def logout(request):
    auth.logout(request)
    return redirect('/')
