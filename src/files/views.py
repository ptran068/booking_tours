from django.shortcuts import render
from .serializers import FileSerializer, UploadFileSerializer
from rest_framework import status
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from .models import File
import boto3
from botocore.client import Config
from rest_framework.permissions import IsAuthenticated
from middlewares.authentication import AuthenticationJWT
from rest_framework.parsers import MultiPartParser
from .models import File
import datetime

class UploadFile(APIView):
    authentication_classes = [AuthenticationJWT]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        serializer = UploadFileSerializer(data=request.data)
        if serializer.is_valid():
            file = request.FILES['file']
            now = datetime.datetime.now().timestamp()
            key = str(file.name) + '/' + str(now)
            s3 = boto3.resource(
                's3',
                aws_access_key_id = settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY,
                config = Config(signature_version = 's3v4')
            )
            s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(Key=key, Body=file, ACL='public-read')
            link_file = settings.AWS_ORIGINAL_LINK + key
            file_serializer = FileSerializer(data=request.data)
            
            if file_serializer.is_valid():
                file_serializer.save(name=str(file.name), link = link_file)
                return Response(data=file_serializer.data, status=status.HTTP_201_CREATED)

            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

