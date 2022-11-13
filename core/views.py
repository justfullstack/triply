from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from posts.forms import NewPostForm
from groups.models import Group
from posts.models import Post, Image
from django.contrib import messages
import logging


logger = logging.getLogger(__name__)


class HomeView(View):
    def get(self, request):
        new_post_form = NewPostForm()
        user = request.user

        if not user.is_authenticated:
            posts = []

            context = {
                'new_post_form': new_post_form,
                'user': user,
                'posts': posts
            }
        else:

            posts = Post.objects.all()

            context = {
                'new_post_form': new_post_form,
                'user': user,
                'posts': posts
            }

        return render(request, 'index.html', context=context)

    def post(self, request):
        new_post_form = NewPostForm(request.POST, request.FILES)

        user = request.user

        posts = Post.objects.all()

        context = {
            'new_post_form': new_post_form,
            'user': user,
            'posts': posts
        }

        if not user.is_authenticated:
            messages.error(request, "You must be logged in to post!")
            return redirect(reverse("users:login"))

        if new_post_form.is_valid():
            text = request.POST["text"]

            post = Post.objects.create(text=text, user=user)

            images = request.FILES.getlist("images")

            for image in images:
                img = Image.objects.create(
                    image=image,
                    post=post,
                    user=user
                )
                img.save()
            post.save()

            logger.info(f"New post added by {user.username}")
            messages.success(request, "Post added successfully!")

        return render(request, 'index.html', context=context)
