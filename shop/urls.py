from django.urls import path

from .views import ProductListView, ShirtListView

urlpatterns = [
    path("products/", ProductListView.as_view()),
    path("shirts/", ShirtListView.as_view()),
]
