from django.contrib import admin

from .models import CoachingStep, CommunityEvent, Partner, SiteSetting, SiteText, SocialLink


@admin.register(SiteText)
class SiteTextAdmin(admin.ModelAdmin):
    list_display = ("page", "section", "key", "short_text", "note")
    list_filter = ("page", "section")
    search_fields = ("section", "key", "text", "note")
    ordering = ("page", "order", "section", "key")
    list_per_page = 60

    @admin.display(description="Text")
    def short_text(self, obj):
        return (obj.text[:90] + "…") if len(obj.text) > 90 else obj.text


@admin.register(CoachingStep)
class CoachingStepAdmin(admin.ModelAdmin):
    list_display = ("number", "title", "anchor_ref")
    ordering = ("number",)


@admin.register(CommunityEvent)
class CommunityEventAdmin(admin.ModelAdmin):
    list_display = ("number", "title", "host", "active", "order")
    list_editable = ("active", "order")


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "credit", "order", "active")
    list_editable = ("order", "active")


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "order", "active")
    list_editable = ("url", "order", "active")


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ("key", "value", "note")
    search_fields = ("key", "value")
