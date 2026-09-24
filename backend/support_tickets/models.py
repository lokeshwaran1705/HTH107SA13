from django.db import models


class Ticket(models.Model):

    CATEGORY_CHOICES = [
        ("payment", "Payment"),
        ("login", "Login"),
        ("refund", "Refund"),
        ("technical", "Technical"),
        ("delivery", "Delivery"),
        ("account", "Account"),
        ("other", "Other"),
    ]

    URGENCY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    RISK_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    STATUS_CHOICES = [
        ("open", "Open"),
        ("assigned", "Assigned"),
        ("in_progress", "In Progress"),
        ("resolved", "Resolved"),
        ("escalated", "Escalated"),
    ]

    customer_name = models.CharField(max_length=100)

    message = models.TextField()

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="other"
    )

    urgency = models.CharField(
        max_length=10,
        choices=URGENCY_CHOICES,
        default="medium"
    )

    # Frustration detection
    frustration_score = models.IntegerField(default=0)

    frustration_level = models.CharField(
        max_length=10,
        default="low"
    )

    # Duplicate detection
    is_duplicate = models.BooleanField(default=False)

    duplicate_ticket_id = models.IntegerField(
        null=True,
        blank=True
    )

    duplicate_similarity = models.FloatField(
        default=0
    )

    sla_deadline = models.DateTimeField()

    sla_risk = models.CharField(
        max_length=10,
        choices=RISK_CHOICES,
        default="low"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="open"
    )

    assigned_agent = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer_name} - {self.category}"


class Agent(models.Model):

    name = models.CharField(max_length=100)

    skills = models.JSONField(default=list)

    current_load = models.IntegerField(default=0)

    capacity = models.IntegerField(default=5)

    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name