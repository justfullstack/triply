

from django.urls import path, include
from . import views


app_name = "profiles"

urlpatterns = [
    path(
        'user/<slug:slug>/follow',
        views.follow,
        name='follow-user'
    ),

    path(
        'user/<slug:slug>/unfollow',
        views.unfollow,
        name='unfollow-user'
    ),

    path(
        'user/<slug:slug>/',
        views.UserDetailView.as_view(),
        name='user'
    ),

    path(
        '',
        views.UserListView.as_view(),
        name='users'
    ),





]
