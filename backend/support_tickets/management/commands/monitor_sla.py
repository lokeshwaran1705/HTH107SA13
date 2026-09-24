import time
from django.core.management.base import BaseCommand
from support_tickets.models import Ticket
from support_tickets.sla_engine import calculate_sla_risk


class Command(BaseCommand):
    help = "Continuously monitors active tickets and updates SLA risk / escalation status"

    def handle(self, *args, **options):
        self.stdout.write("SLA monitor started...")
        while True:
            active_tickets = Ticket.objects.exclude(
                status__in=["Resolved", "Escalated"]
            )

            for ticket in active_tickets:
                old_risk = ticket.sla_risk
                new_risk = calculate_sla_risk(ticket)

                if new_risk != old_risk:
                    ticket.sla_risk = new_risk
                    ticket.save(update_fields=["sla_risk"])
                    self.stdout.write(
                        f"Ticket #{ticket.id}: risk {old_risk} → {new_risk}"
                    )

                if new_risk == "high" and ticket.status != "Escalated":
                    ticket.status = "Escalated"
                    ticket.save(update_fields=["status"])
                    self.stdout.write(
                        self.style.WARNING(f"Ticket #{ticket.id} ESCALATED")
                    )

            time.sleep(30)  # check every 30 seconds