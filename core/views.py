from django.shortcuts import render
from django.views import View
from posts.forms import NewPostForm
from groups.models import Group
from posts.models import Post, Image
from django.contrib import messages


class HomeView(View):
    def get(self, request):
        new_post_form = NewPostForm()
        user = request.user

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

            messages.success(request, "Post added successfully!")

        return render(request, 'index.html', context=context)
