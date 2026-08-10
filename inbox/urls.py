from django.urls import path

from .views import ClubJoinView, ContactView, SubscribeView

urlpatterns = [
    path("contact/", ContactView.as_view()),
    path("club/join/", ClubJoinView.as_view()),
    path("subscribe/", SubscribeView.as_view()),
]
