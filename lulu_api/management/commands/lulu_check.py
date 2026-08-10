"""
Verify the whole Lulu setup BEFORE a real order can trigger a print job.

    python manage.py lulu_check                # uses the .env values
    python manage.py lulu_check --pages 107    # override the page count

Checks, in order:
  1. Credentials      — can we get an OAuth token with the key/secret?
  2. File URLs        — can Lulu actually download the interior + cover PDFs?
  3. pod_package_id   — is the SKU valid, and what does printing cost?
  4. Shipping levels  — which options are available to a US address?

Nothing is ordered and nothing is charged — this only asks Lulu for a quote.
"""
import requests
from django.conf import settings
from django.core.management.base import BaseCommand

from lulu_api.services import _base_url, _token, cost_calculation, shipping_options

# a real US address, only used to get a shipping quote
TEST_ADDRESS = {
    "name": "Test Buyer",
    "street1": "101 Independence Ave SE",
    "city": "Washington",
    "state_code": "DC",
    "postcode": "20540",
    "country_code": "US",
    "phone_number": "+1 702 555 0100",
}


class Command(BaseCommand):
    help = "Validate the Lulu credentials, print files, SKU and shipping before going live."

    def add_arguments(self, parser):
        parser.add_argument("--pages", type=int, default=107, help="Interior page count (default: 107).")
        parser.add_argument("--quantity", type=int, default=1)
        parser.add_argument("--sku", default=None, help="Try a different pod_package_id without editing .env (e.g. a paperback SKU).")
        parser.add_argument("--shipping", default=None, help="Try a different shipping level: MAIL, PRIORITY_MAIL, GROUND, EXPEDITED, EXPRESS.")
        parser.add_argument("--price", type=float, default=None, help="Your sale price — prints the profit after Lulu and Square fees.")

    def handle(self, *args, **options):
        pages = options["pages"]
        qty = options["quantity"]
        sku = options["sku"] or settings.LULU_POD_PACKAGE_ID
        shipping_level = options["shipping"] or settings.LULU_SHIPPING_LEVEL
        sale_price = options["price"]
        ok = self.style.SUCCESS("  OK  ")
        bad = self.style.ERROR(" FAIL ")

        mode = "SANDBOX" if settings.LULU_USE_SANDBOX else "PRODUCTION (real money)"
        self.stdout.write(f"\nLulu environment : {mode}")
        self.stdout.write(f"API base         : {_base_url()}")
        self.stdout.write(f"pod_package_id   : {sku}" + ("  (override)" if options["sku"] else ""))
        self.stdout.write(f"shipping level   : {shipping_level}" + ("  (override)" if options["shipping"] else ""))
        self.stdout.write(f"auto print       : {settings.LULU_AUTO_PRINT}\n")

        # ── 1. credentials ──
        self.stdout.write("1. Credentials")
        if not settings.LULU_CLIENT_KEY or not settings.LULU_CLIENT_SECRET:
            self.stdout.write(f"{bad} LULU_CLIENT_KEY / LULU_CLIENT_SECRET are empty in .env")
            return
        try:
            _token()
            self.stdout.write(f"{ok} authenticated with Lulu")
        except Exception as exc:
            self.stdout.write(f"{bad} could not get a token: {exc}")
            self.stdout.write("      → wrong key/secret, or production keys used against sandbox (they are separate accounts)")
            return

        # ── 2. print files ──
        self.stdout.write("\n2. Print files (Lulu downloads these — they must be public)")
        for label, url in (("interior", settings.LULU_INTERIOR_URL), ("cover", settings.LULU_COVER_URL)):
            if not url:
                self.stdout.write(f"{bad} LULU_{label.upper()}_URL is empty")
                continue
            try:
                resp = requests.head(url, timeout=20, allow_redirects=True)
                ctype = resp.headers.get("content-type", "?")
                size = int(resp.headers.get("content-length", 0)) / 1_000_000
                if resp.ok and "pdf" in ctype.lower():
                    self.stdout.write(f"{ok} {label}: reachable, {size:.1f} MB")
                elif resp.ok:
                    self.stdout.write(f"{bad} {label}: reachable but content-type is '{ctype}', expected a PDF")
                    self.stdout.write("      → on Cloudinary, PDFs must be uploaded as 'raw', not 'image'")
                else:
                    self.stdout.write(f"{bad} {label}: HTTP {resp.status_code} — Lulu cannot download it")
            except requests.RequestException as exc:
                self.stdout.write(f"{bad} {label}: unreachable ({exc})")

        # ── 3. SKU + cost ──
        self.stdout.write(f"\n3. Product SKU & cost ({qty}× {pages} pages)")
        line_items = [{"page_count": pages, "pod_package_id": sku, "quantity": qty}]
        try:
            quote = cost_calculation(line_items, TEST_ADDRESS, shipping_level=shipping_level)
            printing = quote.get("line_item_costs", [{}])[0].get("total_cost_excl_tax") or quote.get("total_cost_excl_tax")
            shipping = (quote.get("shipping_cost") or {}).get("total_cost_excl_tax", "?")
            total = quote.get("total_cost_incl_tax", "?")
            self.stdout.write(f"{ok} SKU accepted by Lulu")
            self.stdout.write(f"      printing : ${printing}")
            self.stdout.write(f"      shipping : ${shipping}  ({shipping_level})")
            self.stdout.write(self.style.WARNING(f"      TOTAL COST TO PACITA PER ORDER: ${total}"))
            if sale_price:
                cost = float(total)
                square_fee = sale_price * 0.029 + 0.30
                profit = sale_price - cost - square_fee
                style = self.style.SUCCESS if profit > 0 else self.style.ERROR
                self.stdout.write("")
                self.stdout.write(f"      sale price   : ${sale_price:.2f}")
                self.stdout.write(f"      Lulu cost    : −${cost:.2f}")
                self.stdout.write(f"      Square fee   : −${square_fee:.2f}  (2.9% + 30¢)")
                self.stdout.write(style(f"      HER PROFIT   :  ${profit:.2f} per book  ({profit / sale_price * 100:.0f}% margin)"))
                self.stdout.write("      (tax varies by state — expect ±$1–2 on the Lulu cost)")
            else:
                self.stdout.write("      → re-run with --price 29.99 to see the profit per book")
        except requests.HTTPError as exc:
            body = getattr(exc.response, "text", "")[:400]
            self.stdout.write(f"{bad} Lulu rejected the request: {body}")
            self.stdout.write("      → usually a bad pod_package_id. Get the exact SKU from developers.lulu.com/price-calculator")
            return
        except Exception as exc:
            self.stdout.write(f"{bad} cost calculation failed: {exc}")
            return

        # ── 4. shipping options ──
        self.stdout.write("\n4. Shipping options available to US addresses")
        try:
            options_resp = shipping_options("US")
            levels = sorted({o.get("level") for o in (options_resp if isinstance(options_resp, list) else options_resp.get("results", [])) if o.get("level")})
            self.stdout.write(f"{ok} {', '.join(levels) if levels else 'none returned'}")
            if levels and settings.LULU_SHIPPING_LEVEL not in levels:
                self.stdout.write(self.style.WARNING(f"      ⚠ your LULU_SHIPPING_LEVEL '{settings.LULU_SHIPPING_LEVEL}' is not in that list"))
        except Exception as exc:
            self.stdout.write(f"      (could not list shipping options: {exc})")

        # ── summary ──
        self.stdout.write("\n" + "─" * 60)
        if settings.LULU_USE_SANDBOX:
            self.stdout.write(self.style.SUCCESS("Sandbox looks good. Place one test order end-to-end, watch it in\nthe dashboard's Lulu tab, then switch LULU_USE_SANDBOX=False with\nPRODUCTION keys."))
        else:
            self.stdout.write(self.style.WARNING("PRODUCTION mode. The next paid paperback order will really print\nand really charge the card on file. Make sure a payment method is\nsaved at lulu.com/direct/payments or the job will sit UNPAID."))
        self.stdout.write("")