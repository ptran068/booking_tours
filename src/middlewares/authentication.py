from pyexpat import model

import jwt
from django.conf import settings
from rest_framework import exceptions, status
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from django.middleware.csrf import CsrfViewMiddleware
import re

class CSRFCheck(CsrfViewMiddleware):
    def _reject(self, request, reason):
        return reason


class AuthenticationJWT(BaseAuthentication):
    model = get_user_model()

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != b'token':
            return None            
        try:
            token = auth[1]
            if token == "null":
                msg = 'Null token not allowed'
                raise exceptions.AuthenticationFailed(msg)
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)
    

    def authenticate_credentials(self, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = self.model.objects.get(email=payload['email'])
        except (jwt.DecodeError, model.DoesNotExist):
            raise exceptions.AuthenticationFailed('Invalid token')
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')
        if not user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')
        return (user, payload)


class SessionAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Get the session-based user from the underlying HttpRequest object
        user = getattr(request._request, 'user', None)

        # Unauthenticated, CSRF validation not required
        if not user or not user.is_active:
            return None

        self.enforce_csrf(request)

        # CSRF passed with authenticated user
        return (user, None)

    def enforce_csrf(self, request):
        check = CSRFCheck()
        # populates request.META['CSRF_COOKIE'], which is used in process_view()
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        if reason:
            # CSRF failed, bail with explicit error message
            raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)

