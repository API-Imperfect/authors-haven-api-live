from django.urls import path

from .views import (
    ArticleCreateAPIView,
    ArticleDeleteAPIView,
    ArticleDetailView,
    ArticleListAPIView,
    update_article_api_view,
)

urlpatterns = [
    path("all/", ArticleListAPIView.as_view(), name="all-articles"),
    path("create/", ArticleCreateAPIView.as_view(), name="create-article"),
    path("details/<slug:slug>/", ArticleDetailView.as_view(), name="article-detail"),
    path("delete/<slug:slug>/", ArticleDeleteAPIView.as_view(), name="delete-article"),
    path("update/<slug:slug>/", update_article_api_view, name="update-article"),
]
