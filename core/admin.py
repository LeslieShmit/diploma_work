from django.contrib import admin

from .models import SiteContent, TeamMember


@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    list_display = ("id",)


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "position")
    list_filter = ("position",)
    search_fields = ("last_name", "position")
