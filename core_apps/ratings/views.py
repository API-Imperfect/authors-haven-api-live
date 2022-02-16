from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from core_apps.articles.models import Article

from .exceptions import AlreadyRated, CantRateYourArticle
from .models import Rating


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_article_rating_view(request, article_id):
    author = request.user
    article = Article.objects.get(id=article_id)
    data = request.data

    if article.author == author:
        raise CantRateYourArticle

    already_exists = article.article_ratings.filter(rated_by__pkid=author.pkid).exists()
    if already_exists:
        raise AlreadyRated
    elif data["value"] == 0:
        formatted_response = {"detail": "You can't give a zero rating"}
        return Response(formatted_response, status=status.HTTP_400_BAD_REQUEST)
    else:
        rating = Rating.objects.create(
            article=article,
            rated_by=request.user,
            value=data["value"],
            review=data["review"],
        )

        return Response(
            {"success": "Rating has been added"}, status=status.HTTP_201_CREATED
        )
