from django.urls import path

from .views import LuluWebhookView

urlpatterns = [
    path("webhooks/lulu/", LuluWebhookView.as_view()),
]
