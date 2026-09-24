from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import TicketViewSet, dashboard_stats


router = DefaultRouter()
router.register(r"tickets", TicketViewSet, basename="ticket")


urlpatterns = [
    path("dashboard/", dashboard_stats, name="dashboard"),
]

urlpatterns += router.urls