from django.urls import reverse
from django.db import models
from django.contrib.auth import get_user_model
from authentication.models import CustomUser as User
from django.utils.text import slugify
# User = get_user_model()


class Profile(models.Model):

    slug = models.SlugField(unique=True, null=True, blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    followers = models.ManyToManyField(
        User, related_name='followers',
        blank=True)
    following = models.ManyToManyField(
        User, related_name='following', blank=True)
    city = models.CharField(max_length=50, null=False,
                            blank=False, default="Nairobi")
    country = models.CharField(
        max_length=50, null=False, blank=False, default="Kenya")
    profession = models.CharField(
        max_length=50, null=True, blank=True, default="Self-Employed")

    def __str__(self):
        return f"@{self.user.username}"

    def save(self, *args, **kwargs):
        #self.text_html = misaka.html(self.text)
        if self.slug is None:
            self.slug = slugify(
                f"profile-{self.user.username}")

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "profiles: user",
            kwargs={"slug": self.slug}
        )
