
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from groups.models import Group
from django.utils.text import slugify
from django.utils import timezone


User = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_edited = models.DateTimeField(auto_now=True)
    text = models.TextField(max_length=1000,
                            null=True,
                            blank=True,
                            # editable=False
                            )

    text_html = models.TextField(
        max_length=400,
        null=True,
        blank=True,
        editable=False
    )

    group = models.ForeignKey(
        Group,
        related_name='posts',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    likes = models.PositiveIntegerField(blank=True, default=0)
    likers = models.ManyToManyField(User, related_name="likers")
    dislikes = models.PositiveIntegerField(blank=True, default=0)
    dislikers = models.ManyToManyField(User, related_name="dislikers")

    def __str__(self):
        return f"{self.user.username} on {self.date_created} "

    def save(self, *args, **kwargs):
        #self.text_html = misaka.html(self.text)
        if not self.slug:
            self.slug = slugify(f"{self.user.username}  + {timezone.now()}")
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('posts:post',
                       kwargs={'slug': self.slug}
                       )

    class Meta:
        ordering = ['-date_created', 'user']
        unique_together = [['user', 'text', 'date_created']]


class Image(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to=f'posts/images'
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )


class Comment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    body = models.TextField(
        max_length=200,
        null=True,
        blank=True
    )

    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        #self.text_html = misaka.html(self.text)
        if self.slug is None:
            self.slug = slugify(
                f"{self.user.username}  -comment-  + {timezone.now()}")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"comment by {self.user.username}"

    def get_absolute_url(self):
        return reverse('posts:comment',
                       kwargs={'slug': self.slug}
                       )

    class Meta:
        ordering = ['-created_at', 'user']
        unique_together = [['user', 'body', 'post']]


class CommentReply(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    body = models.TextField(
        max_length=200,
        null=True,
        blank=True
    )

    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        #self.text_html = misaka.html(self.text)
        if self.slug is None:
            self.slug = slugify(
                f"{self.user.username} -comment-reply-  + {timezone.now()}")

        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at', 'user']
        unique_together = [['user', 'body', 'comment']]
