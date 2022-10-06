from distutils.command.upload import upload
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from groups.models import Group
from django.utils.text import slugify


User = get_user_model()




class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_last_edited = models.DateTimeField(auto_now=True, null=True)
    text = models.TextField(max_length=200,
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

    dislikes = models.PositiveIntegerField(blank=True, default=0)

    def __str__(self):
        return f"{self.user.username} on {self.date_created} "

    def save(self, *args, **kwargs):
        #self.text_html = misaka.html(self.text)
        self.slug = slugify(f"{self.user.username}  + {self.date_created}")
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

    def __str__(self):
        return f"comment by {self.user.username}"

    def get_absolute_url(self):
        return reverse('posts:comment',
                       kwargs={'pk': self.pk}
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

    class Meta:
        ordering = ['-created_at', 'user']
        unique_together = [['user', 'body', 'comment']]
