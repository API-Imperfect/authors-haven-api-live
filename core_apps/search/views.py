from drf_haystack import viewsets
from drf_haystack.filters import HaystackAutocompleteFilter
from rest_framework import permissions

from core_apps.articles.models import Article

from .serializers import ArticleSearchSerializer


class SearchArticleView(viewsets.HaystackViewSet):
    permission_classes = [permissions.AllowAny]
    index_models = [Article]
    serializer_class = ArticleSearchSerializer
    filter_backends = [HaystackAutocompleteFilter]
