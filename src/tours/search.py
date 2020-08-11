from elasticsearch_dsl.query import Q, MultiMatch, SF
from .documents import TourDocument


def get_search_query(phrase):
    query = Q(
        'function_score',
        query=MultiMatch(
            fields=['title', 'description', 'address', 'amount', 'views'],
            query=phrase
        ),
  
    )
    return TourDocument.search().query(query)


def search(phrase):
    return get_search_query(phrase).to_queryset()