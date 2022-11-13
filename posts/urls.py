
from django.urls import path
from . import views


app_name = 'posts'


urlpatterns = [

    path(
        "",
        views.PostListView.as_view(),
        name="posts",
    ),

    path(
        "post/<slug:slug>/",
        views.PostDetailView.as_view(),
        name="post",
    ),

    path(
        "post/<slug:slug>/edit/",
        views.PostUpdateView.as_view(),
        name="edit-post",
    ),

    path(
        "post/<slug:slug>/delete/",
        views.PostDeleteView.as_view(),
        name="delete-post",
    ),

    path(
        "post/<slug:slug>/like/",
        views.likePost,
        name="like-post",
    ),

    path(
        "post/<slug:slug>/dislike/",
        views.dislikePost,
        name="dislike-post",
    ),

    path(
        "post/comments/comment/<slug:slug>/",
        views.CommentDetailView.as_view(),
        name="comment",
    ),

    path(
        "post/comments/comment/<slug:slug>/edit",
        views.editComment,
        name="edit-comment",
    ),

    path(
        "post/comments/comment/<slug:slug>/delete",
        # views.DeleteComment.as_view(),
        views.deleteComment,
        name="delete-comment",
    ),

    path(
        "post/comments/comment/reply/<slug:slug>/delete",
        # views.DeleteComment.as_view(),
        views.DeleteCommentReply.as_view(),
        name="delete-comment-reply",
    ),

    path(
        "post/comments/comment/reply/<slug:slug>/edit",
        # views.DeleteComment.as_view(),
        views.EditCommentReply.as_view(),
        name="edit-comment-reply",
    ),


]
