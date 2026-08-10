"""
PT's Gallery — every item is a Cloudinary link. The `order` field IS the
arrangement Pacita approved: the API returns items sorted by it, and the
admin lets her re-order without touching code.
"""
from django.db import models


class GalleryItem(models.Model):
    class MediaType(models.TextChoices):
        PHOTO = "photo", "Photo"
        VIDEO = "video", "Video"

    class Category(models.TextChoices):
        ARTWORK = "Artwork", "Artwork"
        COMMUNITY = "Community", "Community"
        SPEAKING = "Speaking & Media", "Speaking & Media"
        PROFESSIONAL = "professional development", "professional development"

    order = models.PositiveIntegerField(default=0, help_text="Display position — the approved arrangement.")
    media_type = models.CharField(max_length=10, choices=MediaType.choices, default=MediaType.PHOTO)
    src = models.URLField(blank=True, null=True, help_text="Cloudinary URL. Leave empty for a 'coming soon' tile.")
    category = models.CharField(max_length=40, choices=Category.choices)
    title = models.CharField(max_length=160)
    caption = models.CharField(max_length=300, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.order:02d} · {self.title}"
