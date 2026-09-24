from datetime import timedelta

from django.utils import timezone
from rest_framework import viewsets

from .models import Ticket
from .serializers import TicketSerializer
from .automation import classify_ticket
from .sla_engine import calculate_sla_risk
from .routing import assign_agent
from .escalation import escalate_ticket


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all().order_by("-created_at")
    serializer_class = TicketSerializer

    def perform_create(self, serializer):
        message = serializer.validated_data["message"]

        # 1. Classify ticket
        category, urgency = classify_ticket(message)

        # 2. Automatically set SLA duration
        if urgency == "high":
            sla_duration = timedelta(hours=1)
        elif urgency == "medium":
            sla_duration = timedelta(hours=4)
        else:
            sla_duration = timedelta(hours=8)

        sla_deadline = timezone.now() + sla_duration

        # 3. Save ticket
        ticket = serializer.save(
            category=category,
            urgency=urgency,
            sla_deadline=sla_deadline
        )

        # 4. Calculate SLA risk
        ticket.sla_risk = calculate_sla_risk(ticket)

        # 5. Assign agent
        ticket.assigned_agent = assign_agent(category)

        # 6. Save automation results
        ticket.save(
            update_fields=[
                "sla_risk",
                "assigned_agent"
            ]
        )

        # 7. Escalate if necessary
        escalate_ticket(ticket)