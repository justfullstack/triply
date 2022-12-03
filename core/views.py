from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from posts.forms import NewPostForm
from groups.models import Group
from posts.models import Post, Image
from django.contrib import messages
import logging
from django.http import JsonResponse
import json
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin



User = get_user_model()


logger = logging.getLogger(__name__)


class HomeView(View):
    def get(self, request):
        new_post_form = NewPostForm()
        user = request.user

        if not user.is_authenticated:
            messages.info(request, 'Please sign up or log in to view posts!')
            return redirect("users:signup")
        
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


# search views
# def searchUsers(request):
    
#     if request.method == "POST":
#         searchStr = json.loads(request.body).get("searchText")
    
#         foundUsers = (
#                 User.objects.filter(username__istartswith=searchStr) | 
#                 User.objects.filter(username__icontains=searchStr)    
#             )
        
#         users = foundUsers.values()
        
#         return JsonResponse(list(users), safe=False)
        
        
        
        
# def searchGroups(request):
#     if request.method == "POST":
        
#         searchStr = json.loads(request.body).get("searchText")
        
#         foundGroups = (
#                 Group.objects.filter(name__istartswith=searchStr) | 
#                 Group.objects.filter(name__icontains=searchStr)    
#             )
        
#         groups = foundGroups.values()
        
#         return JsonResponse(list(groups), safe=False)
        

# def searchPosts(request):
    
#     if request.method == "POST":
        
#         searchStr = json.loads(request.body).get("searchText")
        
        
#         foundPosts = (
#                 Post.objects.filter(text__icontains=searchStr) 
#             )
        
#         posts = foundPosts.values() 
        
#         return JsonResponse(list(posts), safe=False)


def searchUsers(request):
    if request.method == "POST":
        # search db
        searchStr = json.loads(request.body).get("searchText")

        users = (
            User.objects.filter(username__istartswith=searchStr) | 
            User.objects.filter(username__icontains=searchStr) | 
            User.objects.filter(first_name__istartswith=searchStr) |  
            User.objects.filter(last_name__istartswith=searchStr) | 
            User.objects.filter(last_name__icontains=searchStr) |
            User.objects.filter(last_name__icontains=searchStr)   
        )


        data = users.values()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              

        
        return JsonResponse(list(data), safe=False)
    


def searchGroups(request):
    if request.method == "POST":
        # search db
        searchStr = json.loads(request.body).get("searchText")

        groups = (
            Group.objects.filter(name__istartswith=searchStr) | 
            Group.objects.filter(name__icontains=searchStr)    
        )


        data = groups.values()

        
        return JsonResponse(list(data), safe=False)
    
    
