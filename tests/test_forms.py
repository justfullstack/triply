from django.test import TestCase
from django.core import mail
from django.core.exceptions import ValidationError
from authentication.forms import UserCreationForm


class TestAuthForms(TestCase):
    def test_form_validation_works_correctly(self):

        form = UserCreationForm()
        self.assertIsInstance(form, UserCreationForm)
        self.assertFalse(form.is_bound)

        form = UserCreationForm({
            'first_name': 'First',
            'last_name': 'Last',
            'email': 'email@domain.com',
            'password1': 'abcDE123$',
            'password2': 'aB-cDE123$'
        })

        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())
        self.assertRaises(ValidationError)

        post_data = {
            'first_name': 'Test',
            'last_name': 'Name',
            'email': 'testuser@domain.com',
            'username': 'a_very_uniq_one',
            'password1': 'A$bcDE123$',
            'password2': 'A$bcDE123$'
        }

        form = UserCreationForm(post_data)

        self.assertTrue(form.is_valid())

    def test_valid_signup_form_sends_email(self):
        post_data = {
            'first_name': 'Test',
            'last_name': 'Name',
            'email': 'testuser@domain.com',
            'username': 'a_very_uniq_one',
            'password1': 'A$bcDE123$',
            'password2': 'A$bcDE123$'
        }

        form = UserCreationForm(post_data)

        self.assertTrue(form.is_valid())

        with self.assertLogs('authentication.forms', level='INFO') as logs:
            form.send_mail()
            self.assertEqual(len(mail.outbox), 1)  # sends welcome email
            self.assertEqual(mail.outbox[0].subject, 'Welcome to Triply')
            self.assertEqual(len(logs.output), 2)
