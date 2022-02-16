from django.urls import path

from .views import CommentAPIView, CommentUpdateDeleteAPIView

urlpatterns = [
    path("<slug:slug>/comment/", CommentAPIView.as_view(), name="comments"),
    path(
        "<slug:slug>/comment/<str:id>/",
        CommentUpdateDeleteAPIView.as_view(),
        name="comment",
    ),
]
