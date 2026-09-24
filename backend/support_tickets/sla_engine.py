from django.utils import timezone


def calculate_sla_risk(ticket):
    now = timezone.now()

    remaining_seconds = (
        ticket.sla_deadline - now
    ).total_seconds()

    # Total SLA window based on urgency
    if ticket.urgency == "high":
        total_sla_seconds = 60 * 60       # 1 hour

    elif ticket.urgency == "medium":
        total_sla_seconds = 4 * 60 * 60   # 4 hours

    else:
        total_sla_seconds = 8 * 60 * 60   # 8 hours

    # Already breached
    if remaining_seconds <= 0:
        return "high"

    # Calculate percentage of SLA time remaining
    remaining_percentage = (
        remaining_seconds / total_sla_seconds
    ) * 100

    # Risk thresholds
    if remaining_percentage > 50:
        return "low"

    elif remaining_percentage >= 15:
        return "medium"

    else:
        return "high"