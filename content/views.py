from collections import defaultdict

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CoachingStep, CommunityEvent, Partner, SiteSetting, SiteText, SocialLink


class PageContentView(APIView):
    """GET /api/content/<page>/ → {"hero": {"heading": "...", ...}, ...}"""

    def get(self, request, page):
        rows = SiteText.objects.filter(page=page)
        data = defaultdict(dict)
        for row in rows:
            data[row.section][row.key] = row.text
        return Response(data)


class CoachingStepsView(APIView):
    """GET /api/steps/ → the 7 Steps in order."""

    def get(self, request):
        steps = CoachingStep.objects.all()
        return Response([
            {
                "n": f"{s.number:02d}",
                "title": s.title,
                "anchor": s.anchor,
                "anchorRef": s.anchor_ref,
                "copy": s.copy,
            }
            for s in steps
        ])


class CommunityView(APIView):
    """GET /api/community/ → events + partner strip."""

    def get(self, request):
        events = CommunityEvent.objects.filter(active=True)
        partners = Partner.objects.filter(active=True)
        return Response({
            "events": [
                {"n": e.number, "title": e.title, "host": e.host, "copy": e.copy, "partners": e.partners}
                for e in events
            ],
            "partners": [{"name": p.name, "credit": p.credit or None} for p in partners],
        })


class SiteGlobalsView(APIView):
    """GET /api/globals/ → contact info, socials, settings for nav/footer/contact page."""

    def get(self, request):
        settings_map = {s.key: s.value for s in SiteSetting.objects.all()}
        socials = [{"name": s.name, "url": s.url} for s in SocialLink.objects.filter(active=True)]
        return Response({"settings": settings_map, "socials": socials})
