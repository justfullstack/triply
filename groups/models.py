from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify

User = get_user_model()


class Group(models.Model):
    GROUP_TYPES = (
        ("Public", "Public"),
        ("Private", "Private")
    )

    name = models.CharField(max_length=255, unique=True)
    type = models.CharField(
        max_length=10, choices=GROUP_TYPES,  blank=True, default="Public")
    slug = models.SlugField(allow_unicode=True, unique=True)
    about = models.TextField(blank=True, default='')

    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="admin")

    avatar = models.ImageField(
        null=True,
        blank=True,
        upload_to="groups/avatars",
        default="defaults/avatar.jpg")

    cover = models.ImageField(null=True,
                              blank=True,
                              upload_to="groups/covers",
                              default="defaults/cover.jpg")

    description_html = models.TextField(editable=False, blank=True, default='')
    members = models.ManyToManyField(User, through='GroupMembership')
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name.title()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        #self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('groups:group',
                       kwargs={'slug': self.slug}
                       )

    class Meta:
        ordering = ["date_created", "name"]


class GroupMembership(models.Model):
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='memberships'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_groups'
    )

    date_joined = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"@{self.user.username}"

    class Meta:
        unique_together = [['group', 'user']]
