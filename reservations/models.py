from django.db import models
from django.conf import settings

class Table(models.Model):
    """Модель для отдельного столика"""
    number = models.PositiveIntegerField(verbose_name='Номер столика')
    seats = models.PositiveIntegerField(verbose_name='Количество посадочных мест')

    def __str__(self):
        return f"Столик №{self.number}"

    class Meta:
        verbose_name = 'столик'
        verbose_name_plural = 'столики'
        ordering = ['number',]

class Reservation(models.Model):
    """Модель для отдельного бронирования"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reservations',
        verbose_name='Пользователь'
    )

    table = models.ForeignKey(
        Table,
        on_delete=models.CASCADE,
        related_name='reservations',
        verbose_name='Номер столика'
    )

    reservation_date = models.DateField(verbose_name='Дата бронирования')
    reservation_time = models.TimeField(verbose_name='Время бронирования')
    guests = models.PositiveIntegerField(verbose_name='Количество гостей')
    duration = models.PositiveIntegerField(
        default=2,
        verbose_name='Длительность бронирования (часы)'
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания бронирования')

    is_confirmed = models.BooleanField(default=False, verbose_name='Подтверждено')

    def __str__(self):
        return f'Бронирование на {self.table} на {self.reservation_time} {self.reservation_date}'

    class Meta:
        verbose_name = 'бронирование'
        verbose_name_plural = 'бронирования'
        ordering = ['created_at',]