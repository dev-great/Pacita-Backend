import json
import logging

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order, OrderItem
from .services import (
    PriceError,
    collect_downloads,
    create_payment_link,
    fetch_square_order,
    resolve_item,
    send_ebook_delivery_email,
    send_order_email,
    verify_square_signature,
)

log = logging.getLogger(__name__)


class CheckoutView(APIView):
    """POST /api/checkout/
    body: {"items": [{"id": "book-ebook", "qty": 1}, {"id": "shirt-3--XL", "qty": 2}],
           "customer": {"name": "...", "email": "...", "phone": "+1702..."}}
    → {"checkoutUrl": "https://square.link/..."}
    """

    def post(self, request):
        items_in = request.data.get("items") or []
        customer = request.data.get("customer") or {}
        if not items_in:
            return Response({"error": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        order = Order(
            customer_name=(customer.get("name") or "").strip()[:160],
            customer_email=(customer.get("email") or "").strip()[:254],
            customer_phone=(customer.get("phone") or "").strip()[:40],
        )
        # address captured in the cart (Square's confirmed address from the
        # webhook overwrites this after payment — this is the early copy)
        address = customer.get("address") or {}
        if isinstance(address, dict) and any(address.values()):
            order.shipping_address = {
                "address_line_1": str(address.get("line1", ""))[:255],
                "address_line_2": str(address.get("line2", ""))[:255],
                "locality": str(address.get("city", ""))[:120],
                "administrative_district_level_1": str(address.get("state", ""))[:60],
                "postal_code": str(address.get("zip", ""))[:20],
                "country": str(address.get("country", "US"))[:2].upper() or "US",
            }
        resolved = []
        try:
            for entry in items_in:
                qty = max(1, min(int(entry.get("qty", 1)), 50))
                title, price_cents, is_physical = resolve_item(str(entry.get("id", "")))
                resolved.append(OrderItem(item_id=entry.get("id"), title=title, qty=qty, price_cents=price_cents, is_physical=is_physical))
        except PriceError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        order.total_cents = sum(i.price_cents * i.qty for i in resolved)
        order.has_physical = any(i.is_physical for i in resolved)
        order.save()
        for item in resolved:
            item.order = order
        OrderItem.objects.bulk_create(resolved)

        try:
            link_id, square_order_id, url = create_payment_link(order, resolved)
        except Exception:
            log.exception("Square payment link failed")
            order.delete()
            return Response({"error": "Could not start checkout — please try again."}, status=status.HTTP_502_BAD_GATEWAY)

        order.square_payment_link_id = link_id
        order.square_order_id = square_order_id
        order.payment_link_url = url
        order.save(update_fields=["square_payment_link_id", "square_order_id", "payment_link_url"])
        return Response({"checkoutUrl": url, "orderId": order.pk})


class SquareWebhookView(APIView):
    """POST /api/webhooks/square/ — payment.updated → mark paid, email Pacita,
    optionally auto-create the Lulu print job for printed books."""

    authentication_classes = []

    def post(self, request):
        raw = request.body
        signature = request.headers.get("x-square-hmacsha256-signature", "")
        if not verify_square_signature(raw, signature):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        event = json.loads(raw.decode() or "{}")
        if event.get("type") != "payment.updated":
            return Response({"ok": True})

        payment = (event.get("data") or {}).get("object", {}).get("payment", {})
        if payment.get("status") != "COMPLETED":
            return Response({"ok": True})

        square_order_id = payment.get("order_id")
        order = Order.objects.filter(square_order_id=square_order_id).first()
        if not order:
            log.warning("Webhook for unknown Square order %s", square_order_id)
            return Response({"ok": True})
        order.status = Order.Status.PAID

        # 1) the BUYER gets their eBook download links (only if they bought one)
        if not order.delivered:
            try:
                order.delivered = send_ebook_delivery_email(order)
                if not collect_downloads(order):
                    order.delivered = True  # nothing digital to send — consider it done
            except Exception:
                log.exception("eBook delivery email failed for order %s", order.pk)

        # 2) PACITA gets the order notification (says whether links went out)
        if not order.notified:
            try:
                order.notified = send_order_email(order)
            except Exception:
                log.exception("EmailJS notification failed")
        order.save()

        # enrich with shipping address + buyer email from the full Square order
        try:
            sq_order = fetch_square_order(square_order_id)
            fulfillments = sq_order.get("fulfillments") or []
            if fulfillments:
                recipient = (fulfillments[0].get("shipment_details") or {}).get("recipient") or {}
                order.shipping_address = recipient.get("address") or {}
                order.customer_name = order.customer_name or recipient.get("display_name", "")
                order.customer_phone = order.customer_phone or recipient.get("phone_number", "")
                order.customer_email = order.customer_email or recipient.get("email_address", "")
        except Exception:
            log.exception("Could not fetch Square order details")

        order.status = Order.Status.PAID
        try:
            order.notified = send_order_email(order)
        except Exception:
            log.exception("EmailJS notification failed")
        order.save()

        # Lulu automation: paid printed book (paperback or hardcover) → print job
        if settings.LULU_AUTO_PRINT and order.shipping_address:
            printed = [i for i in order.items.all() if i.is_physical and not i.item_id.startswith("shirt")]
            if printed:
                from lulu_api.services import create_print_job_for_order

                try:
                    create_print_job_for_order(order, printed)
                except Exception:
                    log.exception("Lulu print job failed for order %s", order.pk)

        return Response({"ok": True})