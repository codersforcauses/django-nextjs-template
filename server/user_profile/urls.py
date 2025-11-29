from django.urls import path

from . import views

app_name = "user_profile"
urlpatterns = [
    path("profile/<int:pk>/", views.UserProfileDetail.as_view(), name="profile-detail"),
    path("profile/", views.UserProfileList.as_view(), name="profile-list"),
    path("", views.UserList.as_view(), name="user-list"),
]
