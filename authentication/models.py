from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.text import slugify
from django.urls import reverse


class CustomUserManager(BaseUserManager):
    """A custom manager for our custom authentication model"""

    use_in_migrations = True

    def create_user(self, first_name, last_name, username, email, password=None,  avatar=None, cover=None):

        if not (first_name or last_name):
            raise ValueError(_("At least one  name  required!"))

        if not email:
            raise ValueError(_("Email address is required!"))

        if not username:
            raise ValueError(_("Username is required!"))

        try:
            validate_email(email)

        except ValidationError:
            raise ValueError(_("Invalid email address!"))

        email = self.normalize_email(email)

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            is_active=True

        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password, first_name=None):
        if not username:
            raise ValueError(_("Username is required!"))

        if not password:
            raise ValueError(_("Password is required!"))

        superuser = self.model(username=username)
        superuser.set_password(password)

        # # set permissions
        superuser.is_active = True
        superuser.is_superuser = True
        superuser.is_staff = True
        superuser.is_admin = True

        if not superuser.is_superuser:
            raise ValueError(_("Superuser must have is_superuser=True."))

        if not superuser.is_staff:
            raise ValueError(_("Superuser must have is_staff=True."))

        superuser.save(using=self._db)

        return superuser


class CustomUser(AbstractBaseUser):

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = [('first_name' or 'last_name'), ]

    first_name = models.TextField(
        'First Name',
        max_length=30,
        null=True,
        blank=True
    )

    last_name = models.TextField(
        'Last Name',
        max_length=30,
        null=True,
        blank=True
    )

    username = models.CharField(
        'Username: ',
        max_length=50,
        unique=True,
        null=True,
        blank=True
    )

    email = models.EmailField(
        'A valid email address',
        max_length=200,
        unique=True,
        null=True,
        blank=True
    )

    password = models.TextField(
        'Password',
        max_length=150,
        null=True,
        blank=True
    )

    slug = models.SlugField(
        allow_unicode=True, unique=True, null=True, blank=True)

    avatar = models.ImageField(
        null=True, blank=True,
        upload_to="users/avatars")

    about = models.TextField(
        max_length=200,
        blank=True,
        null=True,
        default="")

    cover = models.ImageField(
        null=True, blank=True,
        upload_to="users/covers")

    # profile = models.ForeignKey(
    #     Profile, on_delete=models.CASCADE, related_name="profile")

    date_joined = models.DateTimeField(
        'date_joined',
        null=True,
        blank=True,
        auto_now_add=True
    )

    last_login = models.DateTimeField(
        'last_login',
        null=True,
        blank=True
    )

    is_active = models.BooleanField(
        default=False,
        null=True,
        blank=True
    )

    is_superuser = models.BooleanField(
        default=False,
        null=True,
        blank=True
    )

    is_admin = models.BooleanField(
        default=False,
        null=True,
        blank=True
    )

    is_staff = models.BooleanField(
        default=False,
        null=True,
        blank=True
    )

    is_employee = models.BooleanField(
        default=False,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["username", "email"]

    def __str__(self):
        return f'@{self.username}'

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app  ?"
        # Simplest possible answer: Yes, always
        return True

    def get_absolute_url(self):
        return reverse('users:user',
                       kwargs={'slug': self.slug}
                       )

    def save(self, *args, **kwargs):
        self.is_staff = self.is_admin

        self.is_employee = self.is_active and (
            self.is_superuser
            or self.is_staff
        )

        self.slug = slugify(self.username)

        super().save(*args, **kwargs)
