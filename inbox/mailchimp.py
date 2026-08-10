"""
Mailchimp sync — every newsletter signup (and Bookish Club join) is upserted
into Pacita's Mailchimp audience so she sees her people there too.

Plain REST (no SDK needed):
  PUT https://<dc>.api.mailchimp.com/3.0/lists/<list_id>/members/<md5(email)>
The <dc> datacenter is the suffix of the API key (e.g. "...-us21" → us21).
Upsert (PUT + md5 hash) means re-subscribing the same email never errors.

Config (.env):
  MAILCHIMP_API_KEY   — Account → Extras → API keys
  MAILCHIMP_LIST_ID   — Audience → Settings → "Audience name and defaults" → Audience ID
  MAILCHIMP_DOUBLE_OPT_IN — True = Mailchimp emails a confirm link first ("pending")
"""
import hashlib
import logging

import requests
from django.conf import settings

log = logging.getLogger(__name__)


def _config():
    api_key = getattr(settings, "MAILCHIMP_API_KEY", "")
    list_id = getattr(settings, "MAILCHIMP_LIST_ID", "")
    if not api_key or "-" not in api_key or not list_id:
        return None
    dc = api_key.rsplit("-", 1)[1]
    return api_key, list_id, dc


def add_subscriber(email: str, first_name: str = "", tags: list[str] | None = None) -> bool:
    """Upsert a contact into the audience. Returns True on success.

    Never raises — Mailchimp being down must not break the signup form
    (the subscriber is always saved in our own database first).
    """
    cfg = _config()
    if not cfg:
        log.info("Mailchimp not configured — skipping sync for %s", email)
        return False
    api_key, list_id, dc = cfg

    email = email.strip().lower()
    subscriber_hash = hashlib.md5(email.encode()).hexdigest()
    status = "pending" if getattr(settings, "MAILCHIMP_DOUBLE_OPT_IN", False) else "subscribed"

    payload = {
        "email_address": email,
        # status_if_new: existing members keep their status (never force-resubscribe
        # someone who unsubscribed — that's a Mailchimp compliance rule)
        "status_if_new": status,
        "merge_fields": {"FNAME": first_name[:50]} if first_name else {},
    }
    if tags:
        payload["tags"] = tags

    try:
        resp = requests.put(
            f"https://{dc}.api.mailchimp.com/3.0/lists/{list_id}/members/{subscriber_hash}",
            json=payload,
            auth=("anystring", api_key),
            timeout=15,
        )
        if resp.ok:
            return True
        log.warning("Mailchimp sync failed for %s: %s %s", email, resp.status_code, resp.text[:300])
        return False
    except requests.RequestException:
        log.exception("Mailchimp unreachable for %s", email)
        return False