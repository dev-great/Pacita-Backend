from django.contrib import admin

from .models import ClubMember, ContactSubmission, Subscriber


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ("created_at", "name", "email", "inquiry_type", "handled")
    list_editable = ("handled",)
    list_filter = ("inquiry_type", "handled")
    search_fields = ("name", "email", "message")
    readonly_fields = ("created_at",)


@admin.register(ClubMember)
class ClubMemberAdmin(admin.ModelAdmin):
    list_display = ("created_at", "name", "email", "current_read")
    search_fields = ("name", "email")


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("created_at", "first_name", "email")
    search_fields = ("first_name", "email")
