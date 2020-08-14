from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Tours
from categories.models import Categories
from users.models import CustomUser
from files.models import File


@registry.register_document
class TourDocument(Document):
    created_by = fields.ObjectField(properties={
        'email': fields.TextField(),
        'phone': fields.TextField(),
    })

    images = fields.ObjectField(properties={
        'name': fields.TextField(),
        'link': fields.TextField(),
    })
 

    class Index:
        name = 'tours'
        settings = {'number_of_shards': 2,
                    'number_of_replicas': 0}

    class Meta:
        model = Tours
        fields = '__all__'
        related_models = [CustomUser, File]
        

    class Django:
        model = Tours
        fields = [
            'title',
            'address',
            'description',
            'views',
            'duration',
            'policy',
        ]
        
        def get_instances_from_related(self, related_instance):
            return self

