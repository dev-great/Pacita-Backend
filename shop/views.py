from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, Shirt


def _serialize(p):
    return {
        "id": p.slug,
        "tag": p.tag,
        "title": p.title,
        "subtitle": p.subtitle,
        "kind": p.kind,
        "formatLabel": p.format_label,
        "bonus": p.bonus,
        "priceCents": p.price_cents,
        "cover": p.cover_url,
        "cta": p.cta,
        "accent": p.accent,
        "comingSoon": p.coming_soon,
        "luluHref": p.lulu_url or None,
        # A $0 eBook is a giveaway — its file link becomes public so the site can
        # offer a one-click download. Paid products NEVER expose ebook_file_url;
        # those links only travel by email after Square confirms payment.
        "downloadUrl": p.ebook_file_url if (p.price_cents == 0 and p.kind == Product.Kind.PDF and p.ebook_file_url and not p.coming_soon) else None,
    }


class ProductListView(APIView):
    """GET /api/products/ → the shop cards, in order.

    A product linked as another product's `print_edition` is nested inside that
    card instead of getting a card of its own.
    """

    def get(self, request):
        products = list(Product.objects.filter(active=True).select_related("print_edition"))
        nested_ids = {p.print_edition_id for p in products if p.print_edition_id}
        cards = []
        for p in products:
            if p.id in nested_ids:
                continue  # rendered inside its companion's card
            data = _serialize(p)
            edition = p.print_edition
            data["printEdition"] = _serialize(edition) if edition and edition.active else None
            cards.append(data)
        return Response(cards)


class ShirtListView(APIView):
    """GET /api/shirts/ → B.O.S.S. Faith Moves colorways."""

    def get(self, request):
        shirts = Shirt.objects.filter(active=True)
        return Response([
            {
                "id": s.slug,
                "name": s.name,
                "color": s.color,
                "swatch": s.swatch,
                "src": s.image_url or None,
                "priceCents": s.price_cents,
                "sizes": Shirt.SIZES,
            }
            for s in shirts
        ])