# Generated by Django 3.1 on 2020-08-09 11:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('files', '0001_initial'),
        ('tours', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='tours',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tours',
            name='images',
            field=models.ManyToManyField(blank=True, null=True, related_name='image_tour', to='files.File'),
        ),
        migrations.AddField(
            model_name='tours',
            name='video_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='files.file'),
        ),
    ]
