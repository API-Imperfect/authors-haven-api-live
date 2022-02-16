import logging

from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from core_apps.articles.models import Article, ArticleViews

from .exceptions import UpdateArticle
from .filters import ArticleFilter
from .pagination import ArticlePagination
from .permissions import IsOwnerOrReadOnly
from .renderers import ArticleJSONRenderer, ArticlesJSONRenderer
from .serializers import (
    ArticleCreateSerializer,
    ArticleSerializer,
    ArticleUpdateSerializer,
)

User = get_user_model()

logger = logging.getLogger(__name__)


class ArticleListAPIView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = Article.objects.all()
    renderer_classes = (ArticlesJSONRenderer,)
    pagination_class = ArticlePagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ArticleFilter
    ordering_fields = ["created_at", "username"]


class ArticleCreateAPIView(generics.CreateAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = ArticleCreateSerializer
    renderer_classes = [ArticleJSONRenderer]

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        data["author"] = user.pkid
        serializer = self.serializer_class(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(
            f"article {serializer.data.get('title')} created by {user.username}"
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ArticleDetailView(APIView):
    renderer_classes = [ArticleJSONRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, slug):
        article = Article.objects.get(slug=slug)
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")

        if not ArticleViews.objects.filter(article=article, ip=ip).exists():
            ArticleViews.objects.create(article=article, ip=ip)

            article.views += 1
            article.save()

        serializer = ArticleSerializer(article, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PATCH"])
@permission_classes([permissions.IsAuthenticated])
def update_article_api_view(request, slug):
    try:
        article = Article.objects.get(slug=slug)
    except Article.DoesNotExist:
        raise NotFound("That article does not exist in our catalog")

    user = request.user
    if article.author != user:
        raise UpdateArticle

    if request.method == "PATCH":
        data = request.data
        serializer = ArticleUpdateSerializer(article, data=data, many=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ArticleDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Article.objects.all()
    lookup_field = "slug"

    def delete(self, request, *args, **kwargs):
        try:
            article = Article.objects.get(slug=self.kwargs.get("slug"))
        except Article.DoesNotExist:
            raise NotFound("That article does not exist in our catalog")

        delete_operation = self.destroy(request)
        data = {}
        if delete_operation:
            data["success"] = "Deletion was successful"

        else:
            data["failure"] = "Deletion failed"

        return Response(data=data)
