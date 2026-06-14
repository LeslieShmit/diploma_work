from django.db import models
from django.conf import settings
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.utils import timezone

class Table(models.Model):
    """Модель для отдельного столика"""

    number = models.PositiveIntegerField(verbose_name="Номер столика")
    seats = models.PositiveIntegerField(verbose_name="Количество посадочных мест")

    def __str__(self):
        return f"Столик №{self.number}"

    class Meta:
        verbose_name = "столик"
        verbose_name_plural = "столики"
        ordering = [
            "number",
        ]


class Reservation(models.Model):
    """Модель для отдельного бронирования"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reservations",
        verbose_name="Пользователь",
    )

    table = models.ForeignKey(
        Table,
        on_delete=models.CASCADE,
        related_name="reservations",
        verbose_name="Номер столика",
    )

    reservation_date = models.DateField(verbose_name="Дата бронирования")
    reservation_time = models.TimeField(verbose_name="Время бронирования")
    guests = models.PositiveIntegerField(verbose_name="Количество гостей")
    duration = models.PositiveIntegerField(
        default=2, verbose_name="Длительность бронирования (часы)"
    )
    notes = models.TextField(blank=True, verbose_name="Заметки")

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата и время создания бронирования"
    )

    is_mady_by_staff = models.BooleanField(
        default=False, verbose_name="Создано менеджером"
    )

    # Определение того, является ли бронирование прошедшим
    @property
    def is_past(self):
        return self.reservation_date < timezone.localdate()

    def clean(self):

        # Проверка количества гостей

        if self.guests > self.table.seats:
            raise ValidationError(
                {
                    "guests": (
                        f"Столик №{self.table.number} рассчитан "
                        f"максимум на {self.table.seats} гостей."
                    )
                }
            )

        # Проверка пересечения бронирований

        start = datetime.combine(
            self.reservation_date,
            self.reservation_time,
        )

        end = start + timedelta(hours=self.duration)

        reservations = Reservation.objects.filter(
            table=self.table,
            reservation_date=self.reservation_date,
        )

        if self.pk:
            reservations = reservations.exclude(pk=self.pk)

        for reservation in reservations:

            existing_start = datetime.combine(
                reservation.reservation_date,
                reservation.reservation_time,
            )

            existing_end = (
                    existing_start +
                    timedelta(hours=reservation.duration)
            )

            if start < existing_end and end > existing_start:
                raise ValidationError(
                    {
                        "reservation_time":
                            "Столик уже забронирован на выбранное время."
                    }
                )

    def __str__(self):
        return f"Бронирование на {self.table} на {self.reservation_time} {self.reservation_date}"

    class Meta:
        verbose_name = "бронирование"
        verbose_name_plural = "бронирования"
        ordering = [
            "created_at",
        ]
