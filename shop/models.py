"""
Shop catalog — books (eBooks sold on-site, paperback via Lulu) and the
B.O.S.S. Faith Moves shirt collection. Pacita can add/edit/hide products
and change prices, covers and copy from the admin.
"""
from django.db import models


class Product(models.Model):
    class Kind(models.TextChoices):
        PDF = "pdf", "eBook (PDF — instant download)"
        PAPERBACK = "paperback", "Paperback (physical — printed by Lulu)"
        HARDCOVER = "hardcover", "Hardcover (physical — printed by Lulu)"

    #: kinds that ship — these require a shipping address and trigger a Lulu print job
    PHYSICAL_KINDS = {"paperback", "hardcover"}

    slug = models.SlugField(unique=True, help_text="Stable id used by the cart & price validation (e.g. 'book-ebook').")
    tag = models.CharField(max_length=60, help_text='Card label, e.g. "The Book" / "New · The 3rd Book"')
    title = models.CharField(max_length=160)
    subtitle = models.CharField(max_length=250, blank=True)
    kind = models.CharField(max_length=12, choices=Kind.choices, default=Kind.PDF)
    format_label = models.CharField(max_length=120, blank=True, help_text='e.g. "eBook only · PDF — instant download"')
    bonus = models.CharField(max_length=300, blank=True, help_text="The extra line under the format.")
    price_cents = models.PositiveIntegerField(default=0, help_text="Price in cents — 999 = $9.99. THE source of truth for checkout.")
    cover_url = models.URLField(blank=True, help_text="Cloudinary (or other) URL of the cover image.")
    cta = models.CharField(max_length=60, default="Add to Cart — eBook")
    accent = models.BooleanField(default=False, help_text="Featured styling on the card.")
    coming_soon = models.BooleanField(default=False)
    lulu_url = models.URLField(blank=True, help_text="If set, the card shows a 'Buy the Paperback on Lulu.com' button.")
    ebook_file_url = models.URLField(blank=True, help_text="PRIVATE download link for fulfillment (never shown publicly).")
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    # ── Editions ──
    # Two formats of one book share a single shop card: the eBook is the card,
    # and its print edition renders as the second (orange) button underneath.
    # The printed edition stays a real Product so checkout still prices it
    # server-side; it just doesn't get a card of its own.
    print_edition = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL, related_name="+",
        limit_choices_to={"kind__in": ["paperback", "hardcover"]},
        help_text="Optional printed edition offered on this same card (e.g. link the eBook to its paperback).",
    )
    bonus_ebook = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL, related_name="+",
        limit_choices_to={"kind": "pdf"},
        help_text="A free eBook delivered with this product (e.g. 7 Faith Moves™ with every book purchase).",
    )

    # ── Lulu print-on-demand (physical products only) ──
    # Each printed product carries its own SKU and files, so a paperback and a
    # hardcover of the same book can be sold side by side. Left blank, these
    # fall back to the LULU_* values in .env.
    lulu_pod_package_id = models.CharField(
        max_length=64, blank=True,
        help_text="Lulu SKU, e.g. 0600X0900.BW.STD.CW.060UW444.MXX — get it from developers.lulu.com/price-calculator",
    )
    lulu_interior_url = models.URLField(blank=True, help_text="Public URL of the interior PDF (Lulu downloads it).")
    lulu_cover_url = models.URLField(blank=True, help_text="Public URL of the full wraparound cover PDF.")
    page_count = models.PositiveIntegerField(default=0, help_text="Interior page count — used for Lulu cost quotes.")

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title

    @property
    def is_physical(self) -> bool:
        return self.kind in self.PHYSICAL_KINDS


class Shirt(models.Model):
    """B.O.S.S. Faith Moves colorways."""

    SIZES = ["S", "M", "L", "XL", "2XL"]

    slug = models.SlugField(unique=True, help_text="e.g. 'shirt-1' — cart ids arrive as 'shirt-1--XL'.")
    name = models.CharField(max_length=60, help_text='e.g. "Design 01"')
    color = models.CharField(max_length=40, help_text='Colorway shown to buyers, e.g. "Royal Blue"')
    swatch = models.CharField(max_length=9, default="#5B2A86", help_text="Hex color for the little dot on the card.")
    image_url = models.URLField(blank=True, help_text="Cloudinary URL of the shirt photo.")
    price_cents = models.PositiveIntegerField(default=2500)
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.name} · {self.color}"