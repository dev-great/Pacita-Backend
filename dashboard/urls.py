from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .crud import (
    EventViewSet,
    GalleryViewSet,
    LuluJobViewSet,
    PartnerViewSet,
    ProductViewSet,
    SettingViewSet,
    ShirtViewSet,
    SiteTextViewSet,
    SocialViewSet,
    StepViewSet,
)
from .views import (
    ContactHandledView,
    InboxOverView,
    LoginView,
    LogoutView,
    OrderResendLinksView,
    OrderStatusView,
    OrdersView,
    StatsView,
)

router = DefaultRouter()
router.register("products", ProductViewSet, basename="manage-products")
router.register("shirts", ShirtViewSet, basename="manage-shirts")
router.register("gallery", GalleryViewSet, basename="manage-gallery")
router.register("texts", SiteTextViewSet, basename="manage-texts")
router.register("steps", StepViewSet, basename="manage-steps")
router.register("events", EventViewSet, basename="manage-events")
router.register("partners", PartnerViewSet, basename="manage-partners")
router.register("socials", SocialViewSet, basename="manage-socials")
router.register("settings", SettingViewSet, basename="manage-settings")
router.register("lulu-jobs", LuluJobViewSet, basename="manage-lulu-jobs")

urlpatterns = [
    path("auth/login/", LoginView.as_view()),
    path("auth/logout/", LogoutView.as_view()),
    path("dashboard/stats/", StatsView.as_view()),
    path("dashboard/orders/", OrdersView.as_view()),
    path("dashboard/orders/<int:pk>/", OrderStatusView.as_view()),
    path("dashboard/inbox/", InboxOverView.as_view()),
    path("dashboard/messages/<int:pk>/", ContactHandledView.as_view()),
    path("dashboard/orders/<int:pk>/resend/", OrderResendLinksView.as_view()),
    path("manage/", include(router.urls)),
]