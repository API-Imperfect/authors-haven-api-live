from django.urls import path
from rest_framework import routers

from .views import SearchArticleView

router = routers.DefaultRouter()
router.register("search", SearchArticleView, basename="search-article")

urlpatterns = [
    path("search/", SearchArticleView.as_view({"get": "list"}), name="search-article")
]
