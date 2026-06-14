from django.urls import path

from .views import (
    AvailabilityView,
    HistoryView,
    ReservationCreateView,
    ReservationDeleteView,
    ReservationDetailView,
    ReservationSuccessView,
    ReservationUpdateView,
    UpcomingView,
)

app_name = "reservations"

urlpatterns = [
    path("availability/", AvailabilityView.as_view(), name="availability"),
    path("create/", ReservationCreateView.as_view(), name="reservation_create"),
    path("<int:pk>/", ReservationDetailView.as_view(), name="reservation_details"),
    path(
        "<int:pk>/delete/", ReservationDeleteView.as_view(), name="reservation_delete"
    ),
    path("<int:pk>/edit/", ReservationUpdateView.as_view(), name="reservation_edit"),
    path("history/", HistoryView.as_view(), name="history"),
    path("upcoming/", UpcomingView.as_view(), name="upcoming"),
    path(
        "reservation/success/",
        ReservationSuccessView.as_view(),
        name="reservation_success",
    ),
]
