from django.urls import path
from . import views


app_name = 'groups'

urlpatterns = [
    path(
        '',
        views.GroupListView.as_view(),
        name='groups'
    ),

    path(
        "group/<slug:slug>/",
        views.GroupDetailView.as_view(),
        name="group",
    ),

    path(
        "create/",
        views.CreateGroup.as_view(),
        name="create-group",
    ),

    path(
        "group/<slug:slug>/edit/",
        views.EditGroup.as_view(),
        name="edit-group",
    ),

    path(
        "group/<slug:slug>/delete/",
        views.DeleteGroup.as_view(),
        name="delete-group",
    ),

    path(
        "group/<slug:slug>/join/",
        views.joinGroup,
        name="join-group",
    ),

    path(
        "group/<slug:slug>/exit/",
        views.exitGroup,
        name="exit-group",
    ),


]
