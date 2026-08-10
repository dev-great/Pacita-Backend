from django.urls import path

from .views import CheckoutView, SquareWebhookView

urlpatterns = [
    path("checkout/", CheckoutView.as_view()),
    path("webhooks/square/", SquareWebhookView.as_view()),
]
