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
            "sla_deadline",
            "sla_risk",
            "status",
            "assigned_agent",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "category",
            "urgency",
            "sla_deadline",
            "sla_risk",
            "status",
            "assigned_agent",
            "created_at",
            "updated_at",
        ]