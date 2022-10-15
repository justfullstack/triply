from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views import (generic,
                          View)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . import models
from . import forms
from profiles.models import Profile




class PostListView(generic.ListView):
    model = models.Post
    template_name = "posts/post_list.html"


class PostDetailView(generic.DetailView):
    model = models.Post
    template_name = "posts/post.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs["slug"]

        new_comment_form = forms.UserCommentForm()

        post = get_object_or_404(models.Post,  slug=slug)

        comments = post.comment_set.all()

        context["post"] = post
        context["comments"] = comments
        context["new_comment_form"] = new_comment_form

        return context

    def post(self, request, *args, **kwargs):
        """ handles comment submitted thru' form"""

        new_comment_form = forms.UserCommentForm(request.POST)

        self.object = self.get_object()

        context = super().get_context_data(**kwargs)

        post = models.Post.objects.filter(slug=self.kwargs["slug"])[0]

        comments = post.comment_set.all()

        context["post"] = post
        context["comments"] = comments
        context["new_comment_form"] = new_comment_form

        if new_comment_form.is_valid():

            body = new_comment_form.cleaned_data["body"]

            if request.user == 'AnonymousUser':
                messages.error(request, f"You must be logged in to comment!")
            else:
                try:
                    comment = models.Comment.objects.create(
                        body=body,
                        user=request.user,
                        post=post
                    )
                    comment.save()
                    post.save()

                    messages.success(request, "Comment added successfully!")

                    return redirect(reverse_lazy("posts:post", kwargs={"slug": comment.post.slug}))
                except Exception as e:
                    # messages.error(request, f"Duplicate comment!")
                    messages.error(request, f"{e}")

            new_comment_form = forms.UserCommentForm()

            context["new_comment_form"] = new_comment_form

            return self.render_to_response(context=context)
        return self.render_to_response(context=context)


class PostUpdateView(generic.UpdateView):
    model = models.Post
    fields = ["text", ]
    template_name = "posts/post_form.html"

    def get_success_url(self):
        messages.success(self.request, "Post updated successfuly!")
        return reverse("posts:post", kwargs={"slug": self.object.slug})


class PostDeleteView(generic.DeleteView):
    model = models.Post
    template_name = "posts/post_confirm_delete.html"

    def get_success_url(self):
        messages.error(self.request, "Post was deleted!")
        return redirect(reverse_lazy("posts:posts"))


# comment views
class CommentDetailView(LoginRequiredMixin, View):
    model = models.Comment
    reply_model = models.CommentReply
    template_name = "posts/comment_reply_form.html"

    def get(self, request, slug):
        form = forms.UserCommentReplyForm()
        slug = slug
        comment = self.model.objects.get(slug=slug)

        context = {
            "form": form,
            "comment": comment
        }

        return render(request, self.template_name, context=context)

    def post(self, request, slug):
        form = forms.UserCommentReplyForm(request.POST)
        slug = slug
        comment = self.model.objects.get(slug=slug)

        context = {
            "form": form,
            "comment": comment
        }

        if form.is_valid():
            body = request.POST["text"]

            comment_reply = self.reply_model.objects.create(
                body=body,
                comment=comment,
                user=request.user
            )
            comment_reply.comment = comment

            comment_reply.save()
            comment.save()

            return redirect(
                reverse(
                    "posts:comment",
                    kwargs={"slug": slug}
                )
            )

        return render(request, self.template_name, context=context)


def editComment(request, slug):
    model = models.Comment
    template_name = "posts/comment_form.html"

    comment = model.objects.get(slug=slug)

    if request.method == "POST":
        form = forms.UserCommentForm(request.POST)

        if form.is_valid():
            new_body = request.POST["text"]
            comment.body = new_body
            comment.save()

            messages.success(request, "Comment updated successfuly!")

            return redirect(
                reverse("posts:post", kwargs={"slug": comment.post.slug})
            )

    else:
        form = forms.UserCommentForm(request.POST)
        comment = model.objects.get(slug=slug)

        context = {
            "form": form,
            "comment": comment
        }
        return render(request,  template_name, context=context)


@login_required
def deleteComment(request, slug):
    template_name = "posts/comment_confirm_delete.html"
    comment = models.Comment.objects.get(slug=slug, user=request.user)
    post_slug = comment.post.slug

    if request.method == "POST":
        form = forms.DeleteCommentForm(request.POST)

        if form.is_valid():
            comment.delete()
            messages.error(request, "Comment deleted!")

            return redirect(
                reverse(
                    "posts:post", kwargs={"slug": post_slug}
                )
            )

    else:
        form = forms.DeleteCommentForm()
        context = {
            "form": form,
            "comment": comment
        }

        return render(request, template_name, context=context)


# @login_required
# def deleteCommentReply(request, slug):
#     template_name = "posts/comment_reply_confirm_delete.html"
#     comment_reply = models.CommentReply.objects.get(slug=slug)
#     post_slug = comment_reply.comment.post.slug

#     if request.method == "POST":
#         form = forms.DeleteCommentForm(request.POST)

#         if form.is_valid():
#             comment_reply.delete()
#             messages.error(request, "Comment reply deleted!")

#             return redirect(
#                 reverse(
#                     "posts:post", kwargs={"slug": post_slug}
#                 )
#             )

#     else:
#         form = forms.DeleteCommentForm()
#         context = {
#             "form": form,
#             "comment": comment_reply
#         }

#         return render(request, template_name, context=context)


class EditCommentReply(LoginRequiredMixin, generic.UpdateView):
    model = models.CommentReply
    fields = ['body']
    template_name = "posts/comment_reply.html"

    def get_success_url(self):
        messages.success(self.request, "Comment reply updated successfuly!")
        return reverse("posts:post", kwargs={"slug": self.object.comment.post.slug})


class DeleteCommentReply(LoginRequiredMixin, generic.DeleteView):
    model = models.CommentReply
    template_name = "posts/comment_reply_confirm_delete.html"

    def get_success_url(self):
        messages.error(self.request, "Comment reply deleted!")
        return reverse("posts:post", kwargs={"slug": self.object.comment.post.slug})


# class DeleteComment(LoginRequiredMixin ,generic.DeleteView):
#     model = models.CommentReply
#     template_name = "posts/comment_reply_confirm_delete.html"

#     def get_success_url(self):
#         messages.error(self.request, "Comment deleted!")
#         return reverse_lazy("posts:posts")


def likePost(request, slug):
    post = models.Post.objects.get(slug=slug)
    liker = request.user

    if liker in post.likers.all():
        pass
    else:
        post.likes += 1
        post.likers.add(liker)

        post.save()
