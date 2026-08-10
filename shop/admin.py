from django.contrib import admin
from django.utils.html import format_html

from .models import Product, Shirt


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "kind", "price_display", "coming_soon", "active", "order")
    list_editable = ("coming_soon", "active", "order")
    list_filter = ("kind", "active", "coming_soon")
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        ("The card", {"fields": ("slug", "tag", "title", "subtitle", "cover_url", "accent", "order", "active")}),
        ("Format & copy", {"fields": ("kind", "format_label", "bonus", "cta", "coming_soon")}),
        ("Editions", {
            "fields": ("print_edition", "bonus_ebook"),
            "description": "print_edition: link an eBook to its printed edition so both sell from one card. "
                           "bonus_ebook: a free eBook that gets emailed with every purchase of this product.",
        }),
        ("Money", {"fields": ("price_cents",)}),
        ("Links & fulfillment", {"fields": ("lulu_url", "ebook_file_url")}),
        ("Lulu print-on-demand (physical products only)", {
            "fields": ("lulu_pod_package_id", "lulu_interior_url", "lulu_cover_url", "page_count"),
            "description": "Leave blank to use the LULU_* defaults from .env. Fill these in when selling more than one printed edition.",
            "classes": ("collapse",),
        }),
    )

    @admin.display(description="Price")
    def price_display(self, obj):
        return f"${obj.price_cents / 100:.2f}"


@admin.register(Shirt)
class ShirtAdmin(admin.ModelAdmin):
    list_display = ("name", "color", "swatch_dot", "price_display", "active", "order")
    list_editable = ("active", "order")
    search_fields = ("name", "color")

    @admin.display(description="Swatch")
    def swatch_dot(self, obj):
        return format_html('<span style="display:inline-block;width:16px;height:16px;border-radius:50%;border:1px solid #999;background:{}"></span>', obj.swatch)

    @admin.display(description="Price")
    def price_display(self, obj):
        return f"${obj.price_cents / 100:.2f}"