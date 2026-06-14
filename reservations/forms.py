from django import forms
from django.utils import timezone
from datetime import datetime

from .mixins import FormStyleMixin
from .models import Reservation

class ReservationForm(FormStyleMixin, forms.ModelForm):
    placeholder_fields = {
        "table": "Выберите столик",
        "guests": "Введите количество гостей",
        "notes": "Введите дополнительную информацию",
        "reservation_date": "Выберите дату",
        "reservation_time": "Выберите время",
        "duration": "Введите длительность бронирования",
    }

    reservation_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control",
            }
        ),
        label="Дата бронирования",
    )

    reservation_time = forms.TimeField(
        widget=forms.TimeInput(
            attrs={
                "type": "time",
                "class": "form-control",
            }
        ),
        label="Время бронирования",
    )

    class Meta:
        model = Reservation
        exclude = ["user", "is_mady_by_staff",]

    def clean(self):
        cleaned_data = super().clean()

        reservation_date = cleaned_data.get("reservation_date")
        reservation_time = cleaned_data.get("reservation_time")

        if reservation_date and reservation_time:

            reservation_datetime = datetime.combine(
                reservation_date,
                reservation_time,
            )

            if reservation_datetime < timezone.localtime().replace(tzinfo=None):
                raise forms.ValidationError(
                    "Нельзя создать бронирование на прошедшее время."
                )

        return cleaned_data

    def clean_duration(self):
        duration = self.cleaned_data["duration"]

        if duration < 1:
            raise forms.ValidationError(
                "Минимальная длительность бронирования — 1 час."
            )

        if duration > 6:
            raise forms.ValidationError(
                "Максимальная длительность бронирования — 6 часов."
            )

        return duration