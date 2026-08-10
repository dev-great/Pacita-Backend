"""
Staff dashboard API — powers the /staff pages on the React site.

Auth: POST /api/auth/login/ with a staff account's username + password →
{token}. All other endpoints require `Authorization: Token <token>` and a
staff user. Create staff accounts with `python manage.py createsuperuser`
(or add users in the Django admin and tick "staff status").
"""
from datetime import timedelta

from django.contrib.auth import authenticate
from django.db.models import Count, Sum
from django.utils import timezone
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView

from inbox.models import ClubMember, ContactSubmission, Subscriber
from lulu_api.models import LuluPrintJob
from orders.models import Order, OrderItem
from shop.models import Product, Shirt
from gallery.models import GalleryItem


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and getattr(request.user, "is_staff", False))


class StaffView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff]


def order_dict(o: Order) -> dict:
    return {
        "id": o.pk,
        "createdAt": o.created_at.isoformat(),
        "status": o.status,
        "customerName": o.customer_name,
        "customerEmail": o.customer_email,
        "customerPhone": o.customer_phone,
        "shippingAddress": o.shipping_address,
        "totalCents": o.total_cents,
        "hasPhysical": o.has_physical,
        "notified": o.notified,
        "delivered": o.delivered,
        "items": [{"title": i.title, "qty": i.qty, "priceCents": i.price_cents, "physical": i.is_physical} for i in o.items.all()],
    }


class LoginView(APIView):
    """POST /api/auth/login/ {username, password} → {token, name} (staff only)."""

    def post(self, request):
        user = authenticate(username=request.data.get("username", ""), password=request.data.get("password", ""))
        if not user or not user.is_staff:
            return Response({"error": "Invalid login — staff accounts only."}, status=status.HTTP_401_UNAUTHORIZED)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "name": user.get_full_name() or user.username})


class LogoutView(StaffView):
    """POST /api/auth/logout/ — invalidates the token."""

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response({"ok": True})


class StatsView(StaffView):
    """GET /api/dashboard/stats/ — everything the overview page shows."""

    def get(self, request):
        paid = Order.objects.filter(status__in=[Order.Status.PAID, Order.Status.FULFILLED])

        # revenue over the last 30 days, per day (for the chart)
        today = timezone.localdate()
        start = today - timedelta(days=29)
        daily = {str(start + timedelta(days=i)): {"revenueCents": 0, "orders": 0} for i in range(30)}
        for o in paid.filter(created_at__date__gte=start):
            key = str(o.created_at.astimezone(timezone.get_current_timezone()).date())
            if key in daily:
                daily[key]["revenueCents"] += o.total_cents
                daily[key]["orders"] += 1

        # top sellers (paid orders only)
        top = (
            OrderItem.objects.filter(order__in=paid)
            .values("title")
            .annotate(qty=Sum("qty"), revenueCents=Sum("price_cents"))
            .order_by("-qty")[:6]
        )

        by_status = {row["status"]: row["n"] for row in Order.objects.values("status").annotate(n=Count("id"))}

        return Response({
            "totals": {
                "revenueCents": paid.aggregate(s=Sum("total_cents"))["s"] or 0,
                "revenue30dCents": sum(d["revenueCents"] for d in daily.values()),
                "orders": Order.objects.count(),
                "paidOrders": paid.count(),
                "ordersByStatus": by_status,
                "subscribers": Subscriber.objects.count(),
                "clubMembers": ClubMember.objects.count(),
                "messages": ContactSubmission.objects.count(),
                "unhandledMessages": ContactSubmission.objects.filter(handled=False).count(),
                "activeProducts": Product.objects.filter(active=True).count(),
                "activeShirts": Shirt.objects.filter(active=True).count(),
                "galleryItems": GalleryItem.objects.filter(active=True).count(),
                "luluJobsInFlight": LuluPrintJob.objects.exclude(status__in=["SHIPPED", "CANCELED", "REJECTED"]).count(),
            },
            "daily": [{"date": k, **v} for k, v in daily.items()],
            "topItems": list(top),
            "recentOrders": [order_dict(o) for o in Order.objects.prefetch_related("items")[:8]],
        })


class OrdersView(StaffView):
    """GET /api/dashboard/orders/?status=paid — full order list (newest first)."""

    def get(self, request):
        qs = Order.objects.prefetch_related("items")
        status_filter = request.query_params.get("status")
        if status_filter:
            qs = qs.filter(status=status_filter)
        return Response([order_dict(o) for o in qs[:200]])


class OrderStatusView(StaffView):
    """PATCH /api/dashboard/orders/<id>/ {status} — e.g. mark fulfilled."""

    def patch(self, request, pk):
        order = Order.objects.filter(pk=pk).first()
        if not order:
            return Response(status=status.HTTP_404_NOT_FOUND)
        new_status = request.data.get("status")
        if new_status not in Order.Status.values:
            return Response({"error": f"status must be one of {Order.Status.values}"}, status=status.HTTP_400_BAD_REQUEST)
        order.status = new_status
        order.save(update_fields=["status"])
        return Response(order_dict(order))

class OrderResendLinksView(StaffView):
    """POST /api/dashboard/orders/<id>/resend/ — re-email the eBook download links.

    For when a buyer says "I never got my download" (spam folder, typo'd email
    that Pacita has since corrected on the order, etc.).
    """

    def post(self, request, pk):
        from orders.services import collect_downloads, send_ebook_delivery_email

        order = Order.objects.filter(pk=pk).first()
        if not order:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if not collect_downloads(order):
            return Response({"error": "This order has no downloadable files."}, status=status.HTTP_400_BAD_REQUEST)
        if not order.customer_email:
            return Response({"error": "No email address on this order."}, status=status.HTTP_400_BAD_REQUEST)
        sent = send_ebook_delivery_email(order)
        if sent and not order.delivered:
            order.delivered = True
            order.save(update_fields=["delivered"])
        return Response({"sent": sent, "to": order.customer_email})
    
class InboxOverView(StaffView):
    """GET /api/dashboard/inbox/ — messages, club members, subscribers."""

    def get(self, request):
        return Response({
            "messages": [
                {"id": m.pk, "createdAt": m.created_at.isoformat(), "name": m.name, "email": m.email,
                 "phone": m.phone, "inquiryType": m.inquiry_type, "message": m.message, "handled": m.handled}
                for m in ContactSubmission.objects.all()[:200]
            ],
            "clubMembers": [
                {"id": m.pk, "createdAt": m.created_at.isoformat(), "name": m.name, "email": m.email, "currentRead": m.current_read}
                for m in ClubMember.objects.all()[:500]
            ],
            "subscribers": [
                {"id": s.pk, "createdAt": s.created_at.isoformat(), "firstName": s.first_name, "email": s.email}
                for s in Subscriber.objects.all()[:500]
            ],
        })


class ContactHandledView(StaffView):
    """PATCH /api/dashboard/messages/<id>/ {handled: true|false}."""

    def patch(self, request, pk):
        msg = ContactSubmission.objects.filter(pk=pk).first()
        if not msg:
            return Response(status=status.HTTP_404_NOT_FOUND)
        msg.handled = bool(request.data.get("handled", True))
        msg.save(update_fields=["handled"])
        return Response({"ok": True, "handled": msg.handled})