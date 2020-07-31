from rest_framework import serializers
from .models import File
from rest_framework import exceptions
from django.conf import settings
from .services import FileService

class FileSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required = False)

    class Meta:
        model = File
        fields = ['id', 'name', 'link', 'file']

    def validate(self, attrs):
        attrs = super().validate(attrs)
        file = attrs.pop('file')
        if file:
            file_type = file.content_type.split('/')[1]
            if file_type not in settings.FILE_FORMAT:
                raise exceptions.ValidationError('File type is not supported')
            if file.size > settings.UPLOAD_FILE_MAX_SIZE:
                raise exceptions.ValidationError('File size is too large')
        return attrs

    def save(self, file):
        return FileService.upload(file = file)

