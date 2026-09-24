from django.utils import timezone


def calculate_sla_risk(ticket):
    now = timezone.now()

    remaining_seconds = (
        ticket.sla_deadline - now
    ).total_seconds()

    remaining_minutes = remaining_seconds / 60

    # Critical: SLA already breached
    if remaining_minutes <= 0:
        return "high"

    # High urgency tickets
    if ticket.urgency == "high":
        if remaining_minutes <= 60:
            return "high"
        elif remaining_minutes <= 240:
            return "medium"
        else:
            return "low"

    # Medium urgency tickets
    if ticket.urgency == "medium":
        if remaining_minutes <= 60:
            return "high"
        elif remaining_minutes <= 180:
            return "medium"
        else:
            return "low"

    # Low urgency tickets
    if remaining_minutes <= 30:
        return "high"
    elif remaining_minutes <= 120:
        return "medium"

    return "low"