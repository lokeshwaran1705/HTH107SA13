from datetime import timedelta

from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Ticket
from .serializers import TicketSerializer
from .automation import classify_ticket
from .frustration_engine import calculate_frustration
from .duplicate_detector import find_duplicate_ticket
from .sla_engine import calculate_sla_risk
from .routing import assign_agent
from .escalation import escalate_ticket
from .dashboard import get_dashboard_stats


class TicketViewSet(viewsets.ModelViewSet):

    queryset = Ticket.objects.all().order_by("-created_at")
    serializer_class = TicketSerializer

    def perform_create(self, serializer):

        # --------------------------------
        # 1. Get customer message
        # --------------------------------
        message = serializer.validated_data["message"]

        # --------------------------------
        # 2. Ticket Classification
        # --------------------------------
        category, urgency = classify_ticket(message)

        # --------------------------------
        # 3. Frustration Detection
        # --------------------------------
        frustration = calculate_frustration(message)

        frustration_score = frustration["score"]
        frustration_level = frustration["level"]

        # --------------------------------
        # 4. Duplicate Detection
        # --------------------------------
        duplicate = find_duplicate_ticket(message)

        is_duplicate = duplicate["is_duplicate"]

        duplicate_ticket_id = None
        duplicate_similarity = 0

        if duplicate:
            duplicate_ticket_id = duplicate["ticket_id"]
            duplicate_similarity = float(
                duplicate["similarity"]
            )

        # --------------------------------
        # 5. SLA Duration
        # --------------------------------
        if urgency == "high":
            sla_duration = timedelta(hours=1)

        elif urgency == "medium":
            sla_duration = timedelta(hours=4)

        else:
            sla_duration = timedelta(hours=8)

        sla_deadline = timezone.now() + sla_duration

        # --------------------------------
        # 6. Create Ticket
        # --------------------------------
        ticket = serializer.save(
            category=category,
            urgency=urgency,
            frustration_score=frustration_score,
            frustration_level=frustration_level,
            is_duplicate=is_duplicate,
            duplicate_ticket_id=duplicate_ticket_id,
            duplicate_similarity=duplicate_similarity,
            sla_deadline=sla_deadline
        )

        # --------------------------------
        # 7. Calculate SLA Risk
        # --------------------------------
        ticket.sla_risk = calculate_sla_risk(ticket)

        # --------------------------------
        # 8. Agent Routing
        # --------------------------------
        ticket.assigned_agent = assign_agent(category)

        # --------------------------------
        # 9. Save Results
        # --------------------------------
        ticket.save(
            update_fields=[
                "frustration_score",
                "frustration_level",
                "is_duplicate",
                "duplicate_ticket_id",
                "duplicate_similarity",
                "sla_risk",
                "assigned_agent"
            ]
        )

        # --------------------------------
        # 10. Automatic Escalation
        # --------------------------------
        escalate_ticket(ticket)


@api_view(["GET"])
def dashboard_stats(request):

    stats = get_dashboard_stats()

    return Response(stats)