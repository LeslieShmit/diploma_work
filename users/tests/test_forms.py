from django.test import TestCase

from users.forms import CustomUserChangeForm, CustomUserCreationForm


class CustomUserCreationFormTestCase(TestCase):

    def test_valid_phone_number(self):
        form = CustomUserCreationForm(
            data={
                "email": "test@example.com",
                "first_name": "Test",
                "last_name": "User",
                "phone_number": "1234567890",
                "password1": "StrongPassword123",
                "password2": "StrongPassword123",
            }
        )

        self.assertTrue(form.is_valid())

    def test_invalid_phone_number(self):
        form = CustomUserCreationForm(
            data={
                "email": "test@example.com",
                "first_name": "Test",
                "last_name": "User",
                "phone_number": "abc123",
                "password1": "StrongPassword123",
                "password2": "StrongPassword123",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("phone_number", form.errors)


class CustomUserChangeFormTestCase(TestCase):

    def test_invalid_phone_number(self):
        form = CustomUserChangeForm(
            data={
                "email": "test@example.com",
                "phone_number": "invalid",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("phone_number", form.errors)
