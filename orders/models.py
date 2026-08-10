from django.db import models


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending (checkout created)"
        PAID = "paid", "Paid"
        FULFILLED = "fulfilled", "Fulfilled"
        CANCELED = "canceled", "Canceled"

    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDING)

    # Square references
    square_order_id = models.CharField(max_length=100, blank=True, db_index=True)
    square_payment_link_id = models.CharField(max_length=100, blank=True)
    payment_link_url = models.URLField(blank=True)

    # Customer (captured at cart + enriched by the Square webhook)
    customer_name = models.CharField(max_length=160, blank=True)
    customer_email = models.EmailField(blank=True)
    customer_phone = models.CharField(max_length=40, blank=True)
    shipping_address = models.JSONField(default=dict, blank=True)

    total_cents = models.PositiveIntegerField(default=0)
    has_physical = models.BooleanField(default=False)
    notified = models.BooleanField(default=False, help_text="Order email sent to Pacita.")
    delivered = models.BooleanField(default=False, help_text="eBook download links emailed to the buyer.")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.pk} · {self.status} · ${self.total_cents / 100:.2f}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    item_id = models.CharField(max_length=100, help_text="Product slug or 'shirt-N--SIZE'.")
    title = models.CharField(max_length=200)
    qty = models.PositiveIntegerField(default=1)
    price_cents = models.PositiveIntegerField(default=0)
    is_physical = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.qty}× {self.title}"
