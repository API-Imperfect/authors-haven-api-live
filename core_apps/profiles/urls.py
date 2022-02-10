from django.urls import path

from .views import (
    FollowUnfollowAPIView,
    ProfileDetailAPIView,
    ProfileListAPIView,
    UpdateProfileAPIView,
    get_my_followers,
)

urlpatterns = [
    path("all/", ProfileListAPIView.as_view(), name="all-profiles"),
    path(
        "user/<str:username>/", ProfileDetailAPIView.as_view(), name="profile-details"
    ),
    path(
        "update/<str:username>/", UpdateProfileAPIView.as_view(), name="profile-update"
    ),
    path("<str:username>/followers/", get_my_followers, name="my-followers"),
    path(
        "<str:username>/follow/",
        FollowUnfollowAPIView.as_view(),
        name="follow-unfollow",
    ),
]
