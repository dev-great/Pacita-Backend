from django.contrib import admin

from .models import LuluPrintJob


@admin.register(LuluPrintJob)
class LuluPrintJobAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "order", "lulu_id", "status", "updated_at")
    list_filter = ("status",)
    search_fields = ("lulu_id", "external_id")
    readonly_fields = ("created_at", "updated_at", "request_payload", "response_payload", "tracking_urls")
