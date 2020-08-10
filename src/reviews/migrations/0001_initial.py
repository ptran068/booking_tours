

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tours', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=20)),
                ('content', models.TextField()),
                ('views', models.IntegerField(blank=True, default=0, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='createdbyuser', to=settings.AUTH_USER_MODEL)),
                ('images', models.ManyToManyField(blank=True, null=True, to='files.File')),
                ('like', models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL)),
                ('tours', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tours.Tours')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
