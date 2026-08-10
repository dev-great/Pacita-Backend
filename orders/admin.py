from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("item_id", "title", "qty", "price_cents", "is_physical")
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "status", "customer_name", "customer_email", "total_display", "has_physical", "notified", "delivered")
    list_filter = ("status", "has_physical", "notified", "delivered")
    search_fields = ("customer_name", "customer_email", "square_order_id")
    readonly_fields = ("created_at", "square_order_id", "square_payment_link_id", "payment_link_url", "total_cents", "shipping_address")
    inlines = [OrderItemInline]
    date_hierarchy = "created_at"

    @admin.display(description="Total")
    def total_display(self, obj):
        return f"${obj.total_cents / 100:.2f}"
