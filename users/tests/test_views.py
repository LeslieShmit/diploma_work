from django.test import TestCase
from django.urls import reverse

from users.models import CustomUser


class UserViewsTestCase(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="user@example.com",
            password="StrongPassword123",
            phone_number="1234567890",
            first_name="Test",
        )

    def test_register_page_opens(self):
        response = self.client.get(reverse("users:register"))

        self.assertEqual(response.status_code, 200)

    def test_register_user(self):
        response = self.client.post(
            reverse("users:register"),
            {
                "email": "new@example.com",
                "first_name": "New",
                "last_name": "User",
                "phone_number": "9999999999",
                "password1": "StrongPassword123",
                "password2": "StrongPassword123",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(CustomUser.objects.filter(email="new@example.com").exists())

    def test_login_page_opens(self):
        response = self.client.get(reverse("users:login"))

        self.assertEqual(response.status_code, 200)

    def test_user_can_login(self):
        response = self.client.post(
            reverse("users:login"),
            {
                "username": "user@example.com",
                "password": "StrongPassword123",
            },
        )

        self.assertEqual(response.status_code, 302)

    # def test_profile_requires_login(self):
    #     response = self.client.get(reverse("users:user_details"))
    #
    #     self.assertEqual(response.status_code, 302)

    # def test_authorized_user_can_open_profile(self):
    #     self.client.login(
    #         username="user@example.com",
    #         password="StrongPassword123",
    #     )
    #
    #     response = self.client.get(reverse("users:user_details"))
    #
    #     self.assertEqual(response.status_code, 200)

    def test_edit_profile_requires_login(self):
        response = self.client.get(reverse("users:edit_profile"))

        self.assertEqual(response.status_code, 302)

    def test_authorized_user_can_open_edit_page(self):
        self.client.login(
            username="user@example.com",
            password="StrongPassword123",
        )

        response = self.client.get(reverse("users:edit_profile"))

        self.assertEqual(response.status_code, 200)

    def test_user_can_edit_profile(self):
        self.client.login(
            username="user@example.com",
            password="StrongPassword123",
        )

        response = self.client.post(
            reverse("users:edit_profile"),
            {
                "email": "updated@example.com",
                "phone_number": "1111111111",
                "first_name": "Updated",
                "last_name": "User",
            },
        )

        self.user.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.email, "updated@example.com")

    def test_logout(self):
        self.client.login(
            username="user@example.com",
            password="StrongPassword123",
        )

        response = self.client.get(reverse("users:logout"))
