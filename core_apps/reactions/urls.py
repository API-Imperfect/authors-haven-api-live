from django.urls import path

from . import views

urlpatterns = [
    path("<slug:slug>/", views.ReactionAPIView.as_view(), name="user-reaction")
]
