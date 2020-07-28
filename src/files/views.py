from .serializers import FileSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from middlewares.authentication import AuthenticationJWT

class UploadFile(APIView):
    authentication_classes = [AuthenticationJWT]
    permission_classes = [IsAuthenticated]

    def post(self, request, format = None):
        serializer = FileSerializer(data = request.data)
        if serializer.is_valid(raise_exception = True):
            file = serializer.save(file = request.data['file'])
            data = {
                'name': file.name,
                'link': file.link
            }
            return Response(data = data, status = status.HTTP_201_CREATED)

