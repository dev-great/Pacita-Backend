"""
Square + EmailJS services.

Prices are ALWAYS taken from the database (Product / Shirt), never from the
client — the frontend cart only sends ids and quantities.
"""
import base64
import hashlib
import hmac
import logging
import uuid

import requests
from django.conf import settings

from shop.models import Product, Shirt

log = logging.getLogger(__name__)

SQUARE_BASE = {
    "production": "https://connect.squareup.com",
    "sandbox": "https://connect.squareupsandbox.com",
}


class PriceError(Exception):
    pass


def resolve_item(item_id: str):
    """Return (title, unit_price_cents, is_physical) for a cart item id.

    Shirt ids arrive as 'shirt-3--XL' — the size suffix is stripped for lookup
    but kept in the title so Pacita knows what to fulfill.
    """
    base_id, _, size = item_id.partition("--")
    shirt = Shirt.objects.filter(slug=base_id, active=True).first()
    if shirt:
        title = f"B.O.S.S. Faith Moves — {shirt.color}" + (f" · {size}" if size else "")
        return title, shirt.price_cents, True
    product = Product.objects.filter(slug=base_id, active=True, coming_soon=False).first()
    if product:
        # paperback AND hardcover ship — both need an address and a print job
        return product.title, product.price_cents, product.is_physical
    raise PriceError(f"Unknown or unavailable item: {item_id}")


def create_payment_link(order, items):
    """Create a Square-hosted checkout page for the order; returns its URL."""
    base = SQUARE_BASE.get(settings.SQUARE_ENVIRONMENT, SQUARE_BASE["sandbox"])
    line_items = [
        {
            "name": i.title,
            "quantity": str(i.qty),
            "base_price_money": {"amount": i.price_cents, "currency": "USD"},
        }
        for i in items
    ]
    payload = {
        "idempotency_key": str(uuid.uuid4()),
        "order": {
            "location_id": settings.SQUARE_LOCATION_ID,
            "line_items": line_items,
            "metadata": {
                "site_order_id": str(order.pk),
                "customer_name": order.customer_name[:255] or "-",
                "customer_phone": order.customer_phone[:255] or "-",
            },
        },
        "checkout_options": {
            "ask_for_shipping_address": order.has_physical,
            "redirect_url": settings.SQUARE_REDIRECT_URL,
        },
        "pre_populated_data": {},
    }
    if order.customer_email:
        payload["pre_populated_data"]["buyer_email"] = order.customer_email
    if order.customer_phone.startswith("+"):
        payload["pre_populated_data"]["buyer_phone_number"] = order.customer_phone
    # address captured in the cart → pre-filled on Square's checkout page
    if order.shipping_address:
        payload["pre_populated_data"]["buyer_address"] = {
            k: v for k, v in order.shipping_address.items() if v
        }

    resp = requests.post(
        f"{base}/v2/online-checkout/payment-links",
        json=payload,
        headers={"Authorization": f"Bearer {settings.SQUARE_ACCESS_TOKEN}", "Content-Type": "application/json"},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()["payment_link"]
    return data["id"], data["order_id"], data["url"]


def verify_square_signature(raw_body: bytes, signature: str) -> bool:
    """HMAC-SHA256 of (notification_url + body) with the webhook signature key."""
    key = settings.SQUARE_WEBHOOK_SIGNATURE_KEY
    url = settings.SQUARE_WEBHOOK_NOTIFICATION_URL
    if not key or not url:
        return settings.DEBUG  # allow in local dev only
    digest = hmac.new(key.encode(), url.encode() + raw_body, hashlib.sha256).digest()
    return hmac.compare_digest(base64.b64encode(digest).decode(), signature or "")


def fetch_square_order(order_id: str) -> dict:
    base = SQUARE_BASE.get(settings.SQUARE_ENVIRONMENT, SQUARE_BASE["sandbox"])
    resp = requests.get(
        f"{base}/v2/orders/{order_id}",
        headers={"Authorization": f"Bearer {settings.SQUARE_ACCESS_TOKEN}"},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json().get("order", {})


def _emailjs_send(template_id: str, params: dict) -> bool:
    """POST one EmailJS template. Returns True on success, never raises."""
    if not settings.EMAILJS_SERVICE_ID or not template_id:
        log.info("EmailJS not configured — skipping template %s", template_id)
        return False
    payload = {
        "service_id": settings.EMAILJS_SERVICE_ID,
        "template_id": template_id,
        "user_id": settings.EMAILJS_PUBLIC_KEY,
        "accessToken": settings.EMAILJS_PRIVATE_KEY,
        "template_params": params,
    }
    try:
        resp = requests.post("https://api.emailjs.com/api/v1.0/email/send", json=payload, timeout=30)
        if not resp.ok:
            log.warning("EmailJS %s failed: %s %s", template_id, resp.status_code, resp.text[:300])
        return resp.ok
    except requests.RequestException:
        log.exception("EmailJS %s unreachable", template_id)
        return False


def format_address(order) -> str:
    addr = order.shipping_address or {}
    return ", ".join(
        str(addr.get(k))
        for k in ("address_line_1", "address_line_2", "locality", "administrative_district_level_1", "postal_code", "country")
        if addr.get(k)
    ) or "— (digital order, no shipping)"


def collect_downloads(order) -> list[tuple[str, str]]:
    """Every file this buyer is entitled to: (title, url).

    Includes each eBook purchased, plus any bonus eBook attached to a product
    they bought — that's how "every book purchase includes the 7 Faith Moves™
    ebook" is actually honoured.
    """
    downloads: list[tuple[str, str]] = []
    seen: set[str] = set()
    for item in order.items.all():
        product = Product.objects.filter(slug=item.item_id.split("--")[0]).select_related("bonus_ebook").first()
        if not product:
            continue
        candidates = []
        if product.kind == Product.Kind.PDF and product.ebook_file_url:
            candidates.append((product.title, product.ebook_file_url))
        bonus = product.bonus_ebook
        if bonus and bonus.ebook_file_url:
            candidates.append((f"{bonus.title} (included free)", bonus.ebook_file_url))
        for title, url in candidates:
            if url not in seen:
                seen.add(url)
                downloads.append((title, url))
    return downloads


def send_order_email(order) -> bool:
    """Notify Pacita — what sold, who bought it, and what SHE has to do."""
    items = list(order.items.all())
    items_text = "\n".join(f"{i.qty}× {i.title} — ${i.price_cents * i.qty / 100:.2f}" for i in items)

    # spell out fulfillment so she knows at a glance what needs her hands
    todo = []
    if any(i.item_id.startswith("shirt") for i in items):
        todo.append("• SHIRT(S) — pack and ship these yourself to the address above.")
    if any(i.is_physical and not i.item_id.startswith("shirt") for i in items):
        todo.append("• PRINTED BOOK — Lulu prints and ships automatically. Track it in your dashboard.")
    if collect_downloads(order):
        todo.append("• eBOOK(S) — download links were emailed to the buyer automatically.")

    return _emailjs_send(settings.EMAILJS_ORDER_TEMPLATE_ID, {
        "order_id": str(order.pk),
        "customer_name": order.customer_name or "—",
        "customer_email": order.customer_email or "—",
        "customer_phone": order.customer_phone or "—",
        "shipping_address": format_address(order),
        "items": items_text,
        "total": f"${order.total_cents / 100:.2f}",
        "fulfillment": "\n".join(todo) or "• Nothing to do — this order is fully automated.",
    })


def send_ebook_delivery_email(order) -> bool:
    """Email the BUYER their download links. No links → no email."""
    downloads = collect_downloads(order)
    if not downloads or not order.customer_email:
        return False
    return _emailjs_send(settings.EMAILJS_DELIVERY_TEMPLATE_ID, {
        "to_email": order.customer_email,
        "customer_name": order.customer_name.split(" ")[0] if order.customer_name else "friend",
        "order_id": str(order.pk),
        # plain-text list, one per line — works in any EmailJS template
        "downloads": "\n".join(f"{title}: {url}" for title, url in downloads),
        # ready-made HTML buttons for a nicer template
        "downloads_html": "".join(
            f'<a href="{url}" style="display:block;margin:0 0 12px;padding:14px 20px;'
            f'background:#D4A03C;color:#0D0A12;font-weight:bold;text-decoration:none;'
            f'font-family:monospace;text-align:center;">⬇ Download {title}</a>'
            for title, url in downloads
        ),
        "note": settings.EBOOK_LINK_NOTE,
    })