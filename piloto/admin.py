from django.contrib import admin
from django.http.request import HttpRequest
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "recipient", "action", "subject")
    readonly_fields = ("id", "recipient", "action", "subject")

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False
