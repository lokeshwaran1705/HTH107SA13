from django.contrib import admin
from .models import Ticket, Agent


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer_name",
        "category",
        "urgency",
        "sla_risk",
        "status",
        "assigned_agent",
        "sla_deadline",
        "created_at",
    )

    list_filter = (
        "category",
        "urgency",
        "sla_risk",
        "status",
    )

    search_fields = (
        "customer_name",
        "message",
        "assigned_agent",
    )

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "current_load",
        "capacity",
        "is_available",
    )

    list_filter = (
        "is_available",
    )

    search_fields = (
        "name",
    )