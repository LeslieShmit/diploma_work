from django.contrib import admin

from .models import Reservation, Table


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("id", "number")
    list_filter = ("seats",)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("id", "table", "reservation_date", "reservation_time", "guests")
    list_filter = (
        "table",
        "reservation_date",
        "guests",
        "created_at",
    )
    search_fields = (
        "table__number",
        "user__email",
    )
