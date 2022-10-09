from django.shortcuts import redirect
from django.views import generic
from . import models
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy, reverse

from posts.models import Post
from profiles.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


User = get_user_model()


class GroupListView(generic.ListView):
    model = models.Group
    template_name = "groups/group_list.html"
    context_object_name = "groups"

    def get_queryset(self):
        groups = self.model.objects.all()
        return groups


class CreateGroup(LoginRequiredMixin, generic.CreateView):
    fields = ['name', 'about', 'type', 'avatar', 'cover']
    model = models.Group
    template_name = "groups/group_form.html"

    def get_success_url(self):
        messages.success(self.request, f"Group '{self.object.name}' created!")
        return reverse("groups:group", kwargs={"slug": self.object.slug})

    def form_valid(self, form):
        form.instance.created_by = self.request.user  # set group admin
        return super().form_valid(form)


class GroupDetailView(generic.DetailView):
    model = models.Group
    template_name = 'groups/group_detail.html'
    context_object_name = "group"

    def get_context_data(self, **kwargs):

        group_posts = Post.objects.filter(group=self.get_object())
        context = super().get_context_data(**kwargs)
        context["posts"] = group_posts
        return context


class EditGroup(LoginRequiredMixin, generic.UpdateView):
    model = models.Group
    fields = ['name', 'about', 'type', 'avatar', 'cover']
    template_name = "groups/group_edit.html"
    context_object_name = "group"

    def get_success_url(self):
        messages.success(self.request, "Group updated successfuly!")
        return reverse_lazy("groups:group", kwargs={"slug": self.object.slug})

    def get_queryset(self):
        """A user can only edit groups they created"""
        return self.model.objects.filter(
            created_by=self.request.user)


class DeleteGroup(LoginRequiredMixin, generic.DeleteView):
    model = models.Group
    template_name = "groups/group_confirm_delete.html"
    context_object_name = "group"

    def get_success_url(self):
        messages.error(self.request, "Group  deleted!")
        return reverse_lazy("groups:groups")

    def get_queryset(self):
        """A user can only delete groups they created"""
        return self.model.objects.filter(
            created_by=self.request.user)


@login_required
def joinGroup(request, slug):
    group = models.Group.objects.get(slug=slug)
    user = request.user
    group.members.add(user)

    group.save()
    messages.success(request, f"You joined {group.name}!")
    return redirect(
        reverse("groups:group", kwargs={'slug': group.slug})
    )


@login_required
def exitGroup(request, slug):
    group = models.Group.objects.get(slug=slug)
    user = request.user
    group.members.remove(user)

    group.save()

    messages.error(request, f"You left the group {group.name}!")

    return redirect(
        reverse("groups:group", kwargs={'slug': group.slug})
    )
