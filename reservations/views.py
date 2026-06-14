from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from .models import Reservation
from .forms import ReservationForm
from datetime import date
from .mixins import OwnerRequiredMixin
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.http import Http404
from django.core.exceptions import PermissionDenied
from .utils import can_view_all_reservations


class AvailabilityView(ListView):
    model = Reservation
    template_name = "reservations/availability.html"
    context_object_name = "reservations"

    def get_queryset(self):
        selected_date = ( self.request.GET.get("date") or date.today() )

        if selected_date:
            return Reservation.objects.filter(
                reservation_date=selected_date
            ).select_related("table")

        return Reservation.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["selected_date"] = self.request.GET.get("date")

        return context

class ReservationUpdateView(OwnerRequiredMixin, UpdateView):
    model = Reservation
    template_name = "reservations/form.html"
    form_class = ReservationForm
    success_url = reverse_lazy("reservations:upcoming")


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Редактировать бронирование"
        context["submit_text"] = "Сохранить изменения"
        context["cancel_url"] = reverse("reservations:availability")
        return context

    def dispatch(self, request, *args, **kwargs):
        reservation = self.get_object()

        if reservation.is_past:
            raise Http404(
                "Нельзя редактировать завершенное бронирование"
            )

        return super().dispatch(
            request,
            *args,
            **kwargs,
        )

class ReservationCreateView(CreateView):
    model = Reservation
    template_name = "reservations/form.html"
    form_class = ReservationForm
    success_url = reverse_lazy("reservations:reservation_success")

    def form_valid(self, form):
        form.instance.user = self.request.user

        if self.request.user.has_perm(
                "reservations.make_phone_reservations"
        ):
            form.instance.is_mady_by_staff = True

        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Создать бронирование"
        context["submit_text"] = "Сохранить"
        context["cancel_url"] = reverse("reservations:availability")
        return context

class ReservationSuccessView(TemplateView):
    template_name = "reservations/reservation_success.html"

class ReservationDetailView(DetailView):
    model = Reservation
    context_object_name = "reservation"
    template_name = "reservations/reservation_detail.html"

    def dispatch(self, request, *args, **kwargs):
        reservation = self.get_object()

        if (
                reservation.user != request.user
                and not can_view_all_reservations(
            request.user
        )
        ):
            raise PermissionDenied

        return super().dispatch(
            request,
            *args,
            **kwargs
        )

class ReservationDeleteView(OwnerRequiredMixin, DeleteView):
    model = Reservation
    template_name = "reservations/confirm_delete.html"
    success_url = reverse_lazy("reservations:upcoming")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = reverse(
            "reservations:reservation_details", args=[self.object.pk]
        )
        return context

    def dispatch(self, request, *args, **kwargs):
        reservation = self.get_object()

        if reservation.is_past:
            raise Http404(
                "Нельзя удалить завершенное бронирование"
            )

        return super().dispatch(
            request,
            *args,
            **kwargs,
        )



class HistoryView(ListView):
    model = Reservation
    context_object_name = "reservations"
    template_name = "reservations/history.html"
    paginate_by = 20

    def get_queryset(self):
        today = timezone.localdate()

        queryset = Reservation.objects.filter(
            reservation_date__lt=today
        ).order_by("-reservation_date", "-reservation_time")

        if can_view_all_reservations(
                self.request.user
        ):
            return queryset

        return queryset.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["date_from"] = self.request.GET.get(
            "date_from", ""
        )

        context["date_to"] = self.request.GET.get(
            "date_to", ""
        )

        return context

class UpcomingView(ListView):
    model = Reservation
    context_object_name = "reservations"
    template_name = "reservations/upcoming.html"
    paginate_by = 20

    def get_queryset(self):
        today = timezone.localdate()

        queryset = Reservation.objects.filter(
            reservation_date__gte=today
        ).order_by("reservation_date", "reservation_time")

        if can_view_all_reservations(
                self.request.user
        ):
            return queryset

        return queryset.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["date_from"] = self.request.GET.get(
            "date_from", ""
        )

        context["date_to"] = self.request.GET.get(
            "date_to", ""
        )

        return context