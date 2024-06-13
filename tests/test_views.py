from django.test import TestCase
from django.urls import reverse
from authentication.forms import UserCreationForm, UserLoginForm
from unittest.mock import patch
from django.contrib import auth
from django.contrib.auth import get_user_model


User = get_user_model()


class TestPostViews(TestCase):
    pass


class TestAuthViews(TestCase):
    def test_user_signup_page_loads_correctly(self):
        response = self.client.get(reverse("users:signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/signup.html")
        self.assertContains(response, "Triply")
        self.assertIsInstance(response.context["form"], UserCreationForm)

    def test_signup_view_works(self):
        post_data = {
            "first_name": "Last",
            "last_name": "Last",
            "email": "user@domain.com",
            "username": "somethin_uniq",
            "password1": "Abcabcabc1@",
            "password2": "Abcabcabc1@",
        }
        with patch.object(UserCreationForm, "send_mail") as mock_send:

            response = self.client.post(
                reverse("users:signup"),
                post_data
            )
        # confirm redirect
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email="user@domain.com").exists())
        mock_send.assert_called()  # will send activation & welcome emails

    def test_login_page_loads(self):
        response = self.client.get(reverse("users:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/login.html")
        self.assertContains(response, "Welcome")
        self.assertIsInstance(response.context["form"], UserLoginForm)

    def test_login_view_works(self):

        # create user
        signup_post_data = {
            "first_name": "",
            "last_name": "Last",
            "email": "user@domain.com",
            "username": "somethin_uniq",
            "password": "Abcabcabc1@",
        }

        user = User.objects.create(**signup_post_data)

        # activate account
        user.is_active = True
        user.save()

        #  try logging in
        login_post_data = {
            "username": "somethin_uniq",
            "password": "Abcabcabc1@",
        }

        response = self.client.post(reverse("users:login"), login_post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(user.is_authenticated)

# class TestProfileViews(TestCase):
#     pass


# class TestGroupViews(TestCase):
#     pass
# #
