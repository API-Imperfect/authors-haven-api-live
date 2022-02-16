from django.urls import path

from .views import create_article_rating_view

urlpatterns = [
    path("<str:article_id>/", create_article_rating_view, name="rate-article")
]
