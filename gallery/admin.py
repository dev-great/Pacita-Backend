from django.contrib import admin
from django.utils.html import format_html

from .models import GalleryItem


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ("order", "thumb", "title", "category", "media_type", "active")
    list_display_links = ("title",)
    list_editable = ("order", "active")
    list_filter = ("category", "media_type", "active")
    search_fields = ("title", "caption")
    ordering = ("order",)
    list_per_page = 60

    @admin.display(description="Preview")
    def thumb(self, obj):
        if obj.src and obj.media_type == "photo":
            return format_html('<img src="{}" style="height:48px;border-radius:4px" />', obj.src)
        return "🎬" if obj.media_type == "video" else "—"
