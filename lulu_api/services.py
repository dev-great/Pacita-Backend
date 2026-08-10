"""
Lulu Print API client (https://api.lulu.com / https://api.sandbox.lulu.com).

Flow: OAuth2 client-credentials → bearer token → REST calls.
Lulu does NOT take the customer's money — we charge via Square, then create a
print job here; Lulu bills the Lulu account (card on file) for print + shipping.
"""
import base64
import logging
import time

import requests
from django.conf import settings

log = logging.getLogger(__name__)

_TOKEN_CACHE = {"token": None, "expires_at": 0.0}


def _base_url() -> str:
    return "https://api.sandbox.lulu.com" if settings.LULU_USE_SANDBOX else "https://api.lulu.com"


def _token() -> str:
    """Client-credentials token, cached until ~60s before expiry."""
    now = time.time()
    if _TOKEN_CACHE["token"] and now < _TOKEN_CACHE["expires_at"] - 60:
        return _TOKEN_CACHE["token"]
    basic = base64.b64encode(f"{settings.LULU_CLIENT_KEY}:{settings.LULU_CLIENT_SECRET}".encode()).decode()
    resp = requests.post(
        f"{_base_url()}/auth/realms/glasstree/protocol/openid-connect/token",
        data={"grant_type": "client_credentials"},
        headers={"Authorization": f"Basic {basic}", "Content-Type": "application/x-www-form-urlencoded"},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    _TOKEN_CACHE["token"] = data["access_token"]
    _TOKEN_CACHE["expires_at"] = now + int(data.get("expires_in", 3600))
    return _TOKEN_CACHE["token"]


def _headers() -> dict:
    return {"Authorization": f"Bearer {_token()}", "Content-Type": "application/json"}


# ── Public API wrappers ──────────────────────────────

def cost_calculation(line_items: list, shipping_address: dict, shipping_level: str | None = None) -> dict:
    """POST /print-job-cost-calculations/ — quote before ordering."""
    payload = {
        "line_items": line_items,
        "shipping_address": shipping_address,
        "shipping_level": shipping_level or settings.LULU_SHIPPING_LEVEL,
    }
    resp = requests.post(f"{_base_url()}/print-job-cost-calculations/", json=payload, headers=_headers(), timeout=60)
    resp.raise_for_status()
    return resp.json()


def shipping_options(iso_country: str = "US") -> dict:
    resp = requests.get(f"{_base_url()}/shipping-options/", params={"iso_country_code": iso_country}, headers=_headers(), timeout=30)
    resp.raise_for_status()
    return resp.json()


def create_print_job(line_items: list, shipping_address: dict, external_id: str = "") -> dict:
    """POST /print-jobs/ — the actual print order."""
    payload = {
        "contact_email": settings.LULU_CONTACT_EMAIL,
        "external_id": external_id,
        "line_items": line_items,
        "shipping_address": shipping_address,
        "shipping_level": settings.LULU_SHIPPING_LEVEL,
    }
    resp = requests.post(f"{_base_url()}/print-jobs/", json=payload, headers=_headers(), timeout=60)
    resp.raise_for_status()
    return resp.json()


def get_print_job(lulu_id: str) -> dict:
    resp = requests.get(f"{_base_url()}/print-jobs/{lulu_id}/", headers=_headers(), timeout=30)
    resp.raise_for_status()
    return resp.json()


def register_webhook(url: str, topics: list[str] | None = None) -> dict:
    """POST /webhooks/ — Lulu will POST status changes to our endpoint."""
    payload = {"topics": topics or ["PRINT_JOB_STATUS_CHANGED"], "url": url}
    resp = requests.post(f"{_base_url()}/webhooks/", json=payload, headers=_headers(), timeout=30)
    resp.raise_for_status()
    return resp.json()


# ── Site-specific helpers ────────────────────────────

def book_line_item(quantity: int = 1, title: str = "The Appointed Time") -> dict:
    """The Appointed Time as a Lulu line item, from the configured files."""
    return {
        "external_id": "appointed-time-paperback",
        "title": title,
        "quantity": quantity,
        "printable_normalization": {
            "interior": {"source_url": settings.LULU_INTERIOR_URL},
            "cover": {"source_url": settings.LULU_COVER_URL},
            "pod_package_id": settings.LULU_POD_PACKAGE_ID,
        },
    }


def square_address_to_lulu(order) -> dict:
    """Convert the Square shipping address saved on our Order to Lulu's format."""
    a = order.shipping_address or {}
    return {
        "name": order.customer_name or "Customer",
        "street1": a.get("address_line_1", ""),
        "street2": a.get("address_line_2", "") or None,
        "city": a.get("locality", ""),
        "state_code": a.get("administrative_district_level_1", ""),
        "postcode": a.get("postal_code", ""),
        "country_code": a.get("country", "US"),
        "phone_number": order.customer_phone or "0000000000",
        "email": order.customer_email or settings.LULU_CONTACT_EMAIL,
    }


def create_print_job_for_order(order, paperback_items) -> "object":
    """Create a Lulu print job for a paid site order containing paperbacks."""
    from .models import LuluPrintJob

    qty = sum(i.qty for i in paperback_items)
    line_items = [book_line_item(quantity=qty)]
    address = square_address_to_lulu(order)
    external_id = f"pacitatiana-order-{order.pk}"

    job = LuluPrintJob.objects.create(order=order, external_id=external_id,
                                      request_payload={"line_items": line_items, "shipping_address": address})
    try:
        data = create_print_job(line_items, address, external_id=external_id)
        job.lulu_id = str(data.get("id", ""))
        job.status = (data.get("status") or {}).get("name", "CREATED")
        job.response_payload = data
    except requests.HTTPError as exc:
        job.status = "ERROR"
        job.status_message = getattr(exc.response, "text", str(exc))[:2000]
        log.exception("Lulu create_print_job failed")
    job.save()
    return job
