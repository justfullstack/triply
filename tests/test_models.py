from django.test import TestCase
from authentication.models import CustomUser


class TestPostModel(TestCase):
    pass


class TestAuthModel(TestCase):
    def testCustomUserAuthWorks(self):

        # create user
        user = CustomUser.objects.create_user(
            first_name="First",
            email="user@gmail.com",
            username="uniq_usr",
            password="my_pAssword!"
        )

        # create superuser
        superuser = CustomUser.objects.create_superuser(
            username="uniq_spr_usr",
            password="my_pAssword!"
        )

        self.assertIsInstance(user, CustomUser)
        self.assertIsInstance(superuser, CustomUser)

        self.assertFalse(user.is_active)  # account needs activation
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_admin)

        self.assertEqual(len(CustomUser.objects.all()), 2)

        CustomUser.objects.filter(email=user.email).update(is_active=True)
        user.refresh_from_db()

        self.assertTrue(user.is_active)


class TestProfileModels(TestCase):
    pass


class TestGroupModels(TestCase):
    pass
