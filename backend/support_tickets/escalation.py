def should_escalate(ticket):
    if ticket.sla_risk == "high":
        return True

    return False


def escalate_ticket(ticket):
    if should_escalate(ticket):
        ticket.status = "escalated"
        ticket.save(update_fields=["status"])
        return True

    return False