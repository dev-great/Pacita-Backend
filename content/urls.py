from django.urls import path

from .views import CoachingStepsView, CommunityView, PageContentView, SiteGlobalsView

urlpatterns = [
    path("content/<str:page>/", PageContentView.as_view()),
    path("steps/", CoachingStepsView.as_view()),
    path("community/", CommunityView.as_view()),
    path("globals/", SiteGlobalsView.as_view()),
]
