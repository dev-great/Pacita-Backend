"""
Staff management API — full CRUD over everything on the site, so the React
dashboard can add/edit/delete without touching the Django admin.

All endpoints live under /api/manage/<resource>/ and require a staff token:
  GET    /api/manage/products/          list
  POST   /api/manage/products/          create
  PATCH  /api/manage/products/<id>/     update (partial)
  DELETE /api/manage/products/<id>/     delete
Resources: products, shirts, gallery, texts (?page=home), steps, events,
partners, socials, settings, lulu-jobs (read-only + POST <id>/refresh/).
"""
import logging

from rest_framework import serializers, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response

from content.models import CoachingStep, CommunityEvent, Partner, SiteSetting, SiteText, SocialLink
from gallery.models import GalleryItem
from lulu_api.models import LuluPrintJob
from shop.models import Product, Shirt

from .views import IsStaff

log = logging.getLogger(__name__)


# ── Serializers (all fields editable) ────────────────
def make_serializer(model_cls, read_only=()):
    class _Serializer(serializers.ModelSerializer):
        class Meta:
            model = model_cls
            fields = "__all__"
            read_only_fields = list(read_only)

    return _Serializer


ProductSerializer = make_serializer(Product)
ShirtSerializer = make_serializer(Shirt)
GallerySerializer = make_serializer(GalleryItem)
SiteTextSerializer = make_serializer(SiteText)
StepSerializer = make_serializer(CoachingStep)
EventSerializer = make_serializer(CommunityEvent)
PartnerSerializer = make_serializer(Partner)
SocialSerializer = make_serializer(SocialLink)
SettingSerializer = make_serializer(SiteSetting)
LuluJobSerializer = make_serializer(LuluPrintJob)


# ── Base viewset: staff-token protected ──────────────
class StaffViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff]


class ProductViewSet(StaffViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ShirtViewSet(StaffViewSet):
    queryset = Shirt.objects.all()
    serializer_class = ShirtSerializer


class GalleryViewSet(StaffViewSet):
    queryset = GalleryItem.objects.all()
    serializer_class = GallerySerializer


class SiteTextViewSet(StaffViewSet):
    serializer_class = SiteTextSerializer

    def get_queryset(self):
        qs = SiteText.objects.all()
        page = self.request.query_params.get("page")
        return qs.filter(page=page) if page else qs


class StepViewSet(StaffViewSet):
    queryset = CoachingStep.objects.all()
    serializer_class = StepSerializer


class EventViewSet(StaffViewSet):
    queryset = CommunityEvent.objects.all()
    serializer_class = EventSerializer


class PartnerViewSet(StaffViewSet):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer


class SocialViewSet(StaffViewSet):
    queryset = SocialLink.objects.all()
    serializer_class = SocialSerializer


class SettingViewSet(StaffViewSet):
    queryset = SiteSetting.objects.all()
    serializer_class = SettingSerializer


class LuluJobViewSet(StaffViewSet):
    """Read-only tracking of Lulu print jobs + on-demand status refresh."""

    queryset = LuluPrintJob.objects.all()
    serializer_class = LuluJobSerializer
    http_method_names = ["get", "post", "head", "options"]  # no edit/delete — Lulu owns the truth

    @action(detail=True, methods=["post"])
    def refresh(self, request, pk=None):
        """POST /api/manage/lulu-jobs/<id>/refresh/ — pull latest status from Lulu."""
        job = self.get_object()
        if not job.lulu_id:
            return Response({"error": "This job was never created at Lulu."}, status=400)
        try:
            from lulu_api.services import get_print_job

            data = get_print_job(job.lulu_id)
            status_obj = data.get("status") or {}
            job.status = status_obj.get("name", job.status)
            job.status_message = str(status_obj.get("message", ""))[:2000]
            urls = []
            for li in data.get("line_items", []):
                urls.extend(li.get("tracking_urls") or [])
            if urls:
                job.tracking_urls = urls
            job.response_payload = data
            job.save()
        except Exception as exc:  # credentials missing / network — report, don't crash
            log.exception("Lulu refresh failed")
            return Response({"error": f"Could not reach Lulu: {exc}"}, status=502)
        return Response(LuluJobSerializer(job).data)