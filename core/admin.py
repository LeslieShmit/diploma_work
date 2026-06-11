from django.contrib import admin
from .models import SiteContent, TeamMember

@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    list_display = ('id',)

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    exclude = ("photo",)
    list_filter = ('position',)
    search_fields = ('surname', 'position')

