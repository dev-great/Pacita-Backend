from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .mailchimp import add_subscriber
from .models import ClubMember, ContactSubmission, Subscriber


class ContactView(APIView):
    """POST /api/contact/ — stores the Let's Talk form (EmailJS still sends the email client-side)."""

    def post(self, request):
        d = request.data
        if not d.get("name") or not d.get("email") or not d.get("message"):
            return Response({"error": "name, email and message are required."}, status=status.HTTP_400_BAD_REQUEST)
        ContactSubmission.objects.create(
            name=str(d.get("name"))[:160],
            email=str(d.get("email"))[:254],
            phone=str(d.get("phone", ""))[:40],
            inquiry_type=str(d.get("inquiryType", ""))[:80],
            message=str(d.get("message"))[:5000],
        )
        return Response({"ok": True}, status=status.HTTP_201_CREATED)


class ClubJoinView(APIView):
    """POST /api/club/join/ — Brown Study Bookish Club™ membership."""

    def post(self, request):
        d = request.data
        if not d.get("email"):
            return Response({"error": "email is required."}, status=status.HTTP_400_BAD_REQUEST)
        member, created = ClubMember.objects.get_or_create(
            email=str(d.get("email")).strip().lower()[:254],
            defaults={"name": str(d.get("name", ""))[:160], "current_read": str(d.get("currentRead", ""))[:200]},
        )
        # sync to Pacita's Mailchimp audience, tagged so she can segment club members
        add_subscriber(member.email, first_name=member.name.split(" ")[0] if member.name else "", tags=["Bookish Club"])
        return Response({"ok": True, "alreadyMember": not created}, status=status.HTTP_201_CREATED)


class SubscribeView(APIView):
    """POST /api/subscribe/ — Join the Journey newsletter."""

    def post(self, request):
        d = request.data
        if not d.get("email"):
            return Response({"error": "email is required."}, status=status.HTTP_400_BAD_REQUEST)
        sub, created = Subscriber.objects.get_or_create(
            email=str(d.get("email")).strip().lower()[:254],
            defaults={"first_name": str(d.get("firstName", ""))[:80]},
        )
        # sync to Pacita's Mailchimp audience ("Join the Journey" tag for segmenting)
        add_subscriber(sub.email, first_name=sub.first_name, tags=["Join the Journey"])
        return Response({"ok": True, "alreadySubscribed": not created}, status=status.HTTP_201_CREATED)