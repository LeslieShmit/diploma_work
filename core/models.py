from django.db import models

class SiteContent(models.Model):
    restaurant_name = models.CharField(max_length=150, verbose_name='Название ресторана')
    services = models.TextField(verbose_name='Перечень предоставляемых услуг')
    history_text = models.TextField(verbose_name='История ресторана')
    mission_text = models.TextField(verbose_name='Миссия')
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name='Номер телефона')
    email = models.EmailField(unique=True, verbose_name="Email")
    main_image = models.ImageField(
        upload_to="images/", blank=True, null=True, verbose_name="Главное изображение"
    )
    hall_plan = models.ImageField(
        upload_to="images/", blank=True, null=True, verbose_name="Схема зала"
    )

    class Meta:
        verbose_name = "Наполнение сайта"
        verbose_name_plural = "Наполнения сайта"

    def __str__(self):
        return "Наполнение сайта"


class TeamMember(models.Model):
    first_name = models.CharField(max_length=15, verbose_name='Имя')
    last_name = models.CharField(max_length=30,  verbose_name='Фамилия')
    position = models.CharField(max_length=30,  verbose_name='Должность')
    photo = models.ImageField(
        upload_to="images/", blank=True, null=True, verbose_name="Фото"
    )

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return f'{self.first_name} {self.last_name}'