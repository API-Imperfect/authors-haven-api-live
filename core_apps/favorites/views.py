from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from core_apps.articles.models import Article
from core_apps.articles.serializers import ArticleCreateSerializer

from .exceptions import AlreadyFavorited
from .models import Favorite
from .serializers import FavoriteSerializer


class FavoriteAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FavoriteSerializer

    def post(self, request, slug):
        data = request.data
        article = Article.objects.get(slug=slug)
        user = request.user

        favorite = Favorite.objects.filter(user=user, article=article.pkid).first()

        if favorite:
            raise AlreadyFavorited
        else:
            data["article"] = article.pkid
            data["user"] = user.pkid
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            data = serializer.data
            data["message"] = "Article added to favorites."
            return Response(data, status=status.HTTP_201_CREATED)


class ListUserFavoriteArticlesAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        Favorites = Favorite.objects.filter(user_id=request.user.pkid)

        favorite_articles = []
        for favorite in Favorites:
            article = Article.objects.get(pkid=favorite.article.pkid)
            article = ArticleCreateSerializer(
                article, context={"article": article.slug, "request": request}
            ).data
            favorite_articles.append(article)
        favorites = {"my_favorites": favorite_articles}
        return Response(data=favorites, status=status.HTTP_200_OK)
