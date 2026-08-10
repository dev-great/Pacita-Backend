from django.db import models


class LuluPrintJob(models.Model):
    """Mirror of a Lulu Print-Job so Pacita can watch print/ship status in the admin."""

    STATUSES = ["CREATED", "REJECTED", "UNPAID", "PAYMENT_IN_PROGRESS", "PRODUCTION_READY",
                "PRODUCTION_DELAYED", "IN_PRODUCTION", "ERROR", "SHIPPED", "CANCELED"]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.ForeignKey("orders.Order", null=True, blank=True, on_delete=models.SET_NULL, related_name="lulu_jobs")
    lulu_id = models.CharField(max_length=100, blank=True, db_index=True)
    external_id = models.CharField(max_length=100, blank=True, help_text="Our order reference sent to Lulu.")
    status = models.CharField(max_length=30, default="CREATED")
    status_message = models.TextField(blank=True)
    tracking_urls = models.JSONField(default=list, blank=True)
    request_payload = models.JSONField(default=dict, blank=True)
    response_payload = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Lulu print job"

    def __str__(self):
        return f"Lulu {self.lulu_id or '(pending)'} · {self.status}"
