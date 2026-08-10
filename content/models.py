"""
Editable site content.

SiteText is the workhorse: every headline, paragraph, label and button text on
the site is a row here, addressed by (page, section, key). The React frontend
fetches /api/content/<page>/ and receives {section: {key: text}} — so Pacita can
change any wording from the admin without a deploy.
"""
from django.db import models


class Page(models.TextChoices):
    GLOBAL = "global", "Global (nav / footer)"
    HOME = "home", "Home"
    AUTHOR = "author", "Author"
    SHOP = "shop", "Shop"
    COACHING = "coaching", "7 Steps Coaching"
    COMMUNITY = "community", "Community"
    GALLERY = "gallery", "PT's Gallery"
    BOOKCLUB = "bookclub", "Brown Study Bookish Club™"
    CONTACT = "contact", "Let's Talk!"


class SiteText(models.Model):
    page = models.CharField(max_length=20, choices=Page.choices, db_index=True)
    section = models.CharField(max_length=60, help_text="Which block of the page this text belongs to (e.g. 'hero').")
    key = models.CharField(max_length=60, help_text="The specific text within the section (e.g. 'heading').")
    text = models.TextField(blank=True)
    note = models.CharField(max_length=200, blank=True, help_text="Where this appears on the site (shown to help editing).")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = [("page", "section", "key")]
        ordering = ["page", "order", "section", "key"]
        verbose_name = "Site text"
        verbose_name_plural = "Site texts (every word on the site)"

    def __str__(self):
        return f"{self.page} · {self.section} · {self.key}"


class CoachingStep(models.Model):
    """The Journey — the 7 Steps with scriptural anchors & mindset shifts."""

    number = models.PositiveIntegerField(unique=True)
    title = models.CharField(max_length=120)
    anchor = models.TextField(help_text="The scripture quote, with quotation marks.")
    anchor_ref = models.CharField(max_length=120, help_text='e.g. "— 2 Corinthians 5:17 (CEV)"')
    copy = models.TextField(help_text="The Mindset Shift paragraph.")

    class Meta:
        ordering = ["number"]

    def __str__(self):
        return f"Step {self.number}: {self.title}"


class CommunityEvent(models.Model):
    """Community collaborations (Brush & Bond, Vision Board Arts, ...)."""

    number = models.CharField(max_length=4, default="01")
    title = models.CharField(max_length=120)
    host = models.CharField(max_length=200, blank=True)
    copy = models.TextField(blank=True)
    partners = models.JSONField(default=list, blank=True, help_text='[{"name": "...", "role": "..."}]')
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "number"]

    def __str__(self):
        return self.title


class Partner(models.Model):
    """'In partnership with' strip on the Community page."""

    name = models.CharField(max_length=160)
    credit = models.CharField(max_length=160, blank=True, help_text='e.g. "Helen Williams · CEO" (leave blank for none)')
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


class SocialLink(models.Model):
    name = models.CharField(max_length=40)  # Instagram, Facebook, TikTok, Email...
    url = models.URLField()
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


class SiteSetting(models.Model):
    """Singleton-ish key/value store for contact info & global settings."""

    key = models.CharField(max_length=60, unique=True)
    value = models.TextField(blank=True)
    note = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["key"]

    def __str__(self):
        return self.key
