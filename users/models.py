from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    phone_number = models.CharField(
        unique=True, max_length=15, verbose_name="Номер телефона"
    )
    first_name = models.CharField(max_length=15, verbose_name="Имя")
    last_name = models.CharField(
        max_length=30, blank=True, null=True, verbose_name="Фамилия"
    )
    avatar = models.ImageField(
        upload_to="avatars/", blank=True, null=True, verbose_name="Аватар"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "phone_number",
        "first_name",
    ]
    objects = CustomUserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email

