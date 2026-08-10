"""
Seed the database with every approved text, product, shirt and gallery item.

    python manage.py seed_site                    # create missing rows, keep admin edits
    python manage.py seed_site --overwrite        # reset seeded TEXT to the approved content
    python manage.py seed_site --reset-catalogue  # also reset products & shirts (destructive)

--overwrite deliberately does NOT touch products or shirts. Once the site is
live, the dashboard owns prices, availability and file links — a re-seed must
never quietly put a product back on sale at the wrong price or flip it back to
"coming soon". Pass --reset-catalogue only when you really mean it.
"""
from django.core.management.base import BaseCommand
from django.db import transaction

from content.models import CoachingStep, CommunityEvent, Partner, SiteSetting, SiteText, SocialLink
from gallery.models import GalleryItem
from shop.models import Product, Shirt

from . import seed_data as D


class Command(BaseCommand):
    help = "Seed the site with the approved content (texts, products, shirts, gallery, steps)."

    def add_arguments(self, parser):
        parser.add_argument("--overwrite", action="store_true", help="Reset existing TEXT rows to the approved content (discards admin copy edits).")
        parser.add_argument("--reset-catalogue", action="store_true", help="Also reset products and shirts — wipes dashboard prices, availability and file links.")

    @transaction.atomic
    def handle(self, *args, **options):
        overwrite = options["overwrite"]
        # the catalogue is only ever reset when asked for explicitly
        reset_catalogue = options["reset_catalogue"]
        created = updated = skipped = 0

        def upsert(model, lookup, defaults, allow_overwrite=None):
            nonlocal created, updated, skipped
            can_overwrite = overwrite if allow_overwrite is None else allow_overwrite
            obj, was_created = model.objects.get_or_create(**lookup, defaults=defaults)
            if was_created:
                created += 1
            elif can_overwrite:
                for k, v in defaults.items():
                    setattr(obj, k, v)
                obj.save()
                updated += 1
            else:
                skipped += 1

        # ── Site texts ──
        for i, (page, section, key, text, note) in enumerate(D.SITE_TEXTS):
            upsert(SiteText, {"page": page, "section": section, "key": key}, {"text": text, "note": note, "order": i})

        # ── Settings & socials ──
        for key, value, note in D.SITE_SETTINGS:
            upsert(SiteSetting, {"key": key}, {"value": value, "note": note})
        for i, (name, url) in enumerate(D.SOCIAL_LINKS):
            upsert(SocialLink, {"name": name}, {"url": url, "order": i})

        # ── Coaching steps ──
        for number, title, anchor, anchor_ref, copy in D.COACHING_STEPS:
            upsert(CoachingStep, {"number": number}, {"title": title, "anchor": anchor, "anchor_ref": anchor_ref, "copy": copy})

        # ── Community ──
        for i, (number, title, host, copy, partners) in enumerate(D.COMMUNITY_EVENTS):
            upsert(CommunityEvent, {"number": number}, {"title": title, "host": host, "copy": copy, "partners": partners, "order": i})
        for i, (name, credit) in enumerate(D.PARTNERS):
            upsert(Partner, {"name": name}, {"credit": credit, "order": i})

        # ── Shop ──
        for p in D.PRODUCTS:
            data = dict(p)
            slug = data.pop("slug")
            upsert(Product, {"slug": slug}, data, allow_overwrite=reset_catalogue)
        # pair each card with its printed edition (eBook card → paperback button)
        for card_slug, print_slug in getattr(D, "PRODUCT_EDITION_LINKS", []):
            card = Product.objects.filter(slug=card_slug).first()
            printed = Product.objects.filter(slug=print_slug).first()
            if card and printed and card.print_edition_id != printed.id:
                card.print_edition = printed
                card.save(update_fields=["print_edition"])
                self.stdout.write(f"Linked {print_slug} as the print edition of {card_slug}.")

        # attach the free bonus eBook that ships with a purchase
        for owner_slug, bonus_slug in getattr(D, "PRODUCT_BONUS_EBOOK_LINKS", []):
            owner = Product.objects.filter(slug=owner_slug).first()
            bonus = Product.objects.filter(slug=bonus_slug).first()
            if owner and bonus and owner.bonus_ebook_id != bonus.id:
                owner.bonus_ebook = bonus
                owner.save(update_fields=["bonus_ebook"])
                self.stdout.write(f"Attached {bonus_slug} as the free bonus eBook of {owner_slug}.")

        # drop products that are no longer offered (e.g. after a format switch)
        retired = Product.objects.filter(slug__in=getattr(D, "RETIRED_PRODUCT_SLUGS", []))
        if retired.exists():
            self.stdout.write(self.style.WARNING(f"Removing retired product(s): {', '.join(retired.values_list('slug', flat=True))}"))
            retired.delete()
        for i, (slug, name, color, swatch, image_url) in enumerate(D.SHIRTS):
            upsert(Shirt, {"slug": slug}, {"name": name, "color": color, "swatch": swatch, "image_url": image_url, "price_cents": D.SHIRT_PRICE_CENTS, "order": i}, allow_overwrite=reset_catalogue)

        # ── Gallery (order = position in Pacita's approved arrangement) ──
        for i, (media_type, src, category, title, caption) in enumerate(D.GALLERY_ITEMS, start=1):
            upsert(GalleryItem, {"order": i}, {"media_type": media_type, "src": src, "category": category, "title": title, "caption": caption})

        self.stdout.write(self.style.SUCCESS(f"Seed complete — created {created}, updated {updated}, left untouched {skipped}."))