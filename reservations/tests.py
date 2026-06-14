from datetime import date, time, timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from reservations.forms import ReservationForm
from reservations.models import Reservation, Table

User = get_user_model()


class ReservationTestCase(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            email="user@test.com",
            phone_number="+79999999999",
            first_name="Ivan",
            password="12345",
        )

        self.other_user = User.objects.create_user(
            email="other@test.com",
            phone_number="+78888888888",
            first_name="Petr",
            password="12345",
        )

        self.table = Table.objects.create(
            number=1,
            seats=4,
        )

    def test_guests_cannot_exceed_table_capacity(self):

        reservation = Reservation(
            user=self.user,
            table=self.table,
            reservation_date=date.today() + timedelta(days=1),
            reservation_time=time(18, 0),
            guests=5,
        )

        with self.assertRaises(ValidationError):
            reservation.full_clean()

    def test_overlapping_reservations_not_allowed(self):

        Reservation.objects.create(
            user=self.user,
            table=self.table,
            reservation_date=date.today() + timedelta(days=1),
            reservation_time=time(18, 0),
            guests=2,
            duration=2,
        )

        reservation = Reservation(
            user=self.user,
            table=self.table,
            reservation_date=date.today() + timedelta(days=1),
            reservation_time=time(19, 0),
            guests=2,
            duration=2,
        )

        with self.assertRaises(ValidationError):
            reservation.full_clean()

    def test_is_past_returns_true_for_old_reservation(self):

        reservation = Reservation.objects.create(
            user=self.user,
            table=self.table,
            reservation_date=date.today() - timedelta(days=1),
            reservation_time=time(18, 0),
            guests=2,
        )

        self.assertTrue(reservation.is_past)

    def test_form_rejects_past_datetime(self):

        form = ReservationForm(
            data={
                "table": self.table.pk,
                "reservation_date": date.today() - timedelta(days=1),
                "reservation_time": "18:00",
                "guests": 2,
                "duration": 2,
                "notes": "",
            }
        )

        self.assertFalse(form.is_valid())

    def test_user_cannot_edit_foreign_reservation(self):

        reservation = Reservation.objects.create(
            user=self.other_user,
            table=self.table,
            reservation_date=date.today() + timedelta(days=1),
            reservation_time=time(18, 0),
            guests=2,
        )

        self.client.force_login(self.user)

        response = self.client.get(
            reverse("reservations:reservation_edit", args=[reservation.pk])
        )

        self.assertEqual(response.status_code, 403)


    def test_availability_page(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("reservations:availability"))

        self.assertEqual(response.status_code, 200)

    def test_create_reservation(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("reservations:reservation_create"),
            {
                "table": self.table.pk,
                "reservation_date": date.today() + timedelta(days=1),
                "reservation_time": "18:00",
                "guests": 2,
                "duration": 2,
                "notes": "",
            },
        )

        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            Reservation.objects.count(),
            1,
        )

    def test_upcoming_view(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("reservations:upcoming"))

        self.assertEqual(response.status_code, 200)

    def test_detail_view(self):
        reservation = Reservation.objects.create(
            user=self.user,
            table=self.table,
            reservation_date=date.today() + timedelta(days=1),
            reservation_time=time(18, 0),
            guests=2,
        )

        self.client.force_login(self.user)

        response = self.client.get(
            reverse(
                "reservations:reservation_details",
                args=[reservation.pk],
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_past_reservation_cannot_be_edited(self):
        reservation = Reservation.objects.create(
            user=self.user,
            table=self.table,
            reservation_date=date.today() - timedelta(days=1),
            reservation_time=time(18, 0),
            guests=2,
        )

        self.client.force_login(self.user)

        response = self.client.get(
            reverse(
                "reservations:reservation_edit",
                args=[reservation.pk],
            )
        )

        self.assertEqual(response.status_code, 404)
