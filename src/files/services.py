from .models import File
from django.conf import settings
import datetime
import boto3

class FileService:

    @classmethod
    def upload(cls, file):
        now = datetime.datetime.now().timestamp()
        key = str(file.name) + '/' + str(now)
        s3_client = boto3.resource('s3')
        s3_client.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(Key = key, Body = file)
        link_file = settings.AWS_ORIGINAL_LINK + key
        data = File.objects.create(name = file.name, link = link_file)
        return data

