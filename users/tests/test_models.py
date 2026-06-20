from django.test import TestCase

from users.models import CustomUser


class CustomUserModelTestCase(TestCase):

    def test_str_returns_email(self):
        user = CustomUser.objects.create(
            email="test@example.com",
            phone_number="1234567890",
            first_name="Test",
        )

        self.assertEqual(str(user), "test@example.com")
