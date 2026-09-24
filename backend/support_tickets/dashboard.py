from .models import Ticket, Agent


def get_dashboard_stats():
    total_tickets = Ticket.objects.count()

    open_tickets = Ticket.objects.filter(
        status="open"
    ).count()

    escalated_tickets = Ticket.objects.filter(
        status="escalated"
    ).count()

    high_risk_tickets = Ticket.objects.filter(
        sla_risk="high"
    ).count()

    agents = []

    for agent in Agent.objects.all():
        agents.append({
            "name": agent.name,
            "load": agent.current_load,
            "capacity": agent.capacity,
            "available": agent.is_available,
        })

    return {
        "total_tickets": total_tickets,
        "open_tickets": open_tickets,
        "escalated_tickets": escalated_tickets,
        "high_risk_tickets": high_risk_tickets,
        "agents": agents,
    }