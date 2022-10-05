from django.contrib.auth import get_user_model
from django.contrib.auth import forms as auth_forms
from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
import logging


logger = logging.getLogger(__name__)


User = get_user_model()


class UserCreationForm(forms.Form):
    first_name = forms.CharField(
        label='First Name...',
        max_length=30,
        required=False
    )

    last_name = forms.CharField(
        label='Last Name...',
        max_length=30,
        required=False
    )

    username = forms.CharField(
        label='Username...',
        max_length=50,
        required=False
    )

    email = forms.EmailField(
        label='Enter a valid email..',
        max_length=60,
        required=False,
        validators=[validators.validate_email, ],
    )

    password1 = forms.CharField(
        label='Password...',
        strip=False,
        widget=forms.PasswordInput(render_value=False),
        min_length=8,
        max_length=60,
        required=False,
    )

    password2 = forms.CharField(
        label='Repeat Password',
        strip=False,
        widget=forms.PasswordInput(render_value=False),
        min_length=8,
        max_length=60,
        required=False,
    )

    def clean_username(self):
        try:
            User.objects.get(username=self.cleaned_data["username"])
            raise ValidationError(
                "User with that  username already registered!")

        except User.DoesNotExist:
            return self.cleaned_data["username"]

    def clean_email(self):
        try:
            User.objects.get(email=self.cleaned_data["email"])
            raise ValidationError("User with that  email already registered!")

        except User.DoesNotExist:
            return self.cleaned_data["email"]

    def clean(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")

        if password1 and password2:
            if password1 != password2:
                raise ValidationError("Passwords must match!")
        else:
            raise ValidationError("Both passwords are required!")

        if not (first_name or last_name):
            raise ValidationError("At least one name  is required!")

        return self.cleaned_data

    def send_mail(self):
        '''sends a new user a welcome email'''

        logger.info(
            f"Sending signup email for {self.cleaned_data['username']}")

        from_email = 'welcome@triply.com'
        to_email = self.cleaned_data.get("email")
        subject = 'Welcome to Triply'
        message = f"Hi {self.cleaned_data.get('first_name').title()},\nThank you for joining Triply, the social app for every  modern travel enthusiast. Explore new destinations, share your moments and meet new travel buddies here. But first, let's activate your accoun. Please check your inbox for an activation email."

        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=[to_email, ],
            fail_silently=False,
            html_message=None
        )

        logger.info(
            f"Signup email successfully sent to {self.cleaned_data['username']}")

    for field in [first_name, last_name, username, email, password1, password2]:
        field.widget.attrs.update({'class': 'form-control'})

    for field in [first_name, last_name, username, email, password1, password2]:
        field.widget.attrs.update({'placeholder': field.label})


class UserLoginForm(forms.Form):

    username = forms.CharField(
        label='Username...',
        max_length=50,
        required=False
    )

    password = forms.CharField(
        label='Password...',
        strip=False,
        widget=forms.PasswordInput(render_value=False),
        min_length=8,
        max_length=60,
        required=False,
    )


class UserProfilecreationForm(forms.Form):
    about = forms.CharField(
        max_length=400, widget=forms.Textarea, required=False)

    avatar = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': False}), required=False)

    cover = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': False}), required=False)

    for field in [about]:
        field.widget.attrs.update({'class': 'form-control px-2'})

    for field in [about]:
        field.widget.attrs.update(
            {"placeholder": "Tell others a little about you..."})
