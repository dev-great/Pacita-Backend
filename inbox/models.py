"""Submissions from the site's forms — kept in the admin so nothing is only in email."""
from django.db import models


class ContactSubmission(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=160)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    inquiry_type = models.CharField(max_length=80, blank=True)
    message = models.TextField()
    handled = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} · {self.inquiry_type or 'General'}"


class ClubMember(models.Model):
    """Brown Study Bookish Club™ sign-ups."""

    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=160)
    email = models.EmailField(unique=True)
    current_read = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.email


class Subscriber(models.Model):
    """'Join the Journey' newsletter sign-ups (home page)."""

    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=80, blank=True)
    email = models.EmailField(unique=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.email
