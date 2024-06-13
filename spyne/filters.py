from django.db.models import Q
from rest_framework.filters import BaseFilterBackend


class HashtagAndTextFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        hashtags = request.query_params.get('hashtags', None)
        text = request.query_params.get('text', None)

        if hashtags:
            hashtags_list = hashtags.split(',')
            hashtag_query = Q()
            for hashtag in hashtags_list:
                hashtag_query |= Q(hashtags__regex=rf'\b{hashtag}\b')
            queryset = queryset.filter(hashtag_query).distinct()

        if text:
            text_query = Q(text__icontains=text)
            queryset = queryset.filter(text_query).distinct()

        return queryset