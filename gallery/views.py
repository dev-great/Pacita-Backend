from rest_framework.response import Response
from rest_framework.views import APIView

from .models import GalleryItem


class GalleryListView(APIView):
    """GET /api/gallery/ → all items in Pacita's approved order."""

    def get(self, request):
        items = GalleryItem.objects.filter(active=True)
        return Response([
            {
                "id": item.id,
                "type": item.media_type,
                "src": item.src,
                "category": item.category,
                "title": item.title,
                "caption": item.caption or None,
            }
            for item in items
        ])
