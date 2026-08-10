import json
import logging

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import LuluPrintJob

log = logging.getLogger(__name__)


class LuluWebhookView(APIView):
    """POST /api/webhooks/lulu/ — PRINT_JOB_STATUS_CHANGED submissions.

    Register it once with lulu_api.services.register_webhook("https://<backend>/api/webhooks/lulu/").
    """

    authentication_classes = []

    def post(self, request):
        try:
            event = json.loads(request.body.decode() or "{}")
        except json.JSONDecodeError:
            return Response(status=400)

        data = event.get("data") or event  # submissions wrap the print-job in "data"
        lulu_id = str(data.get("id", ""))
        if not lulu_id:
            return Response({"ok": True})

        job = LuluPrintJob.objects.filter(lulu_id=lulu_id).first()
        if not job:
            log.info("Lulu webhook for unknown job %s", lulu_id)
            return Response({"ok": True})

        status_obj = data.get("status") or {}
        job.status = status_obj.get("name", job.status)
        job.status_message = str(status_obj.get("message", ""))[:2000]
        # collect tracking URLs from line items when shipped
        urls = []
        for li in data.get("line_items", []):
            urls.extend(li.get("tracking_urls") or [])
        if urls:
            job.tracking_urls = urls
        job.response_payload = data
        job.save()

        if job.status == "SHIPPED" and job.order and job.order.status != "fulfilled":
            job.order.status = "fulfilled"
            job.order.save(update_fields=["status"])
        return Response({"ok": True})
