from rest_framework import serializers
from .models import File
from rest_framework import exceptions

class UploadFileSerializer(serializers.Serializer):
    file = serializers.FileField()
    def validate(self, attrs):
        file = attrs.get('file')
        try:
            if file:
                file_type = file.content_type.split('/')[0]

                if file_type in settings.FILE_FORMAT:
                    if file._size > settings.UPLOAD_FILE_MAX_SIZE:
                        raise exceptions.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.TASK_UPLOAD_FILE_MAX_SIZE), filesizeformat(file._size)))
                else:
                    raise exceptions.ValidationError(_('File type is not supported'))
        except:
            raise exceptions.ValidationError(_('Validation error'))

        return file


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'name', 'link']

