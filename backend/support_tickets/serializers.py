from rest_framework import serializers
from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket

        fields = [
            "id",
            "customer_name",
            "message",
            "category",
            "urgency",
            "frustration_score",
            "frustration_level",
            "is_duplicate",
            "duplicate_ticket_id",
            "duplicate_similarity",
            "sla_deadline",
            "sla_risk",
            "status",
            "assigned_agent",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "category",
            "urgency",
            "frustration_score",
            "frustration_level",
            "sla_deadline",
            "sla_risk",
            "status",
            "assigned_agent",
            "created_at",
            "updated_at",
        ]