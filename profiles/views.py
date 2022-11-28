from django.urls import reverse
from .models import Profile
from posts.models import Post
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import get_user_model
from django.views import generic
from django import views
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import NewPostForm
from posts.forms import UserCommentForm
from posts.models import Post, Image, Comment, CommentReply
from django.contrib import messages
from django.contrib.auth.decorators import login_required


User = get_user_model()


class UserListView(views.View):
    model = User
    template_name = "profiles/user_list.html"

    def get(self, request):

        profiles = Profile.objects.all()
        # current_profile = Profile.objects.get(user=request.user)

        context = {
            "profiles": profiles,
            # "users": users,
            # "current_profile": current_profile
        }

        return render(request, self.template_name, context=context)

    # def post(self, request):
    #     context = {

    #     }

    #     return render(request, self.template_name, context=context)


class UserDetailView(views.View):
    def get(self, request, slug):
        user = User.objects.get(slug=slug)
        posts = Post.objects.filter(user=user)
        profile = Profile.objects.get_or_create(user=user)[0]
        new_post_form = NewPostForm()

        context = {
            "posts": posts,
            "profile":  profile,
            "new_post_form": new_post_form

        }

        return render(request, 'profiles/user_detail.html', context=context)

    def post(self, request, slug):
        user = request.user
        posts = Post.objects.filter(user=user)
        usr_profile = Profile.objects.get(user=user)
        new_post_form = NewPostForm(request.POST, request.FILES)

        # new post form
        if new_post_form.is_valid():
            new_post_text = request.POST['text']
            new_post_images = request.FILES.getlist('images')

            # create post
            if new_post_images is not None:

                post = Post.objects.create(user=user,
                                           text=new_post_text)
                for image in new_post_images:
                    img = Image.objects.create(image=image,
                                               user=user)
                    img.post = post
                    img.save()
                post.save()
                messages.success(request, "Successfully added post!")
                return redirect(reverse("profiles:user", kwargs={"slug": slug}))

            else:
                messages.error(request, "Each post must have an image!")
        else:
            for error in new_post_form.errors:
                messages.error(request, f"{error}")

        context = {
            "posts": posts,
            "usr_profile": usr_profile,
            "new_post_form": new_post_form

        }

        return render(request, 'profiles/user_detail.html', context=context)


@login_required
def follow(request, slug):
    profile = Profile.objects.get_or_create(user=request.user)[0]

    usr_to_follow = User.objects.get(slug=slug)
    usr_to_follow_profile = Profile.objects.get_or_create(user=usr_to_follow)[
        0]

    if usr_to_follow in profile.following.all():
        return redirect(reverse("profiles:users"))

    else:
        profile.following.add(usr_to_follow)
        usr_to_follow_profile.followers.add(usr_to_follow)

        messages.success(
            request, f"You are now following @{usr_to_follow.username}!")

        usr_to_follow_profile.save()
        profile.save()
        return redirect(reverse("profiles:users"))  # , kwargs={"slug": slug})


@ login_required
def unfollow(request, slug):
    profile = Profile.objects.get(user=request.user)

    usr_to_unfollow = User.objects.get(slug=slug)
    usr_to_unfollow_profile = Profile.objects.get(user=usr_to_unfollow)

    if usr_to_unfollow not in profile.following.all():
        return redirect(reverse("profiles:users"))
        # return redirect(reverse("profiles:user", kwargs={"slug": slug}))

    else:
        profile.following.remove(usr_to_unfollow)
        usr_to_unfollow_profile.followers.remove(usr_to_unfollow)

        messages.error(
            request, f"You unfollowed @{usr_to_unfollow.username}!")

        usr_to_unfollow_profile.save()
        profile.save()
        # return redirect(reverse("profiles:user", kwargs={"slug": slug}))
        return redirect(reverse("profiles:users"))
