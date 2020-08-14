from .documents import TourDocument
from elasticsearch_dsl import Q


def get_search_query(phrase):
    query = Q("multi_match", query=phrase, fields=['title', 'address', 'description', 'policy'])
    return TourDocument.search().query(query)


def search(phrase):
    return get_search_query(phrase).to_queryset()
