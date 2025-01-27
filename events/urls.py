from django.urls import path
from events.views import organizer_dashboard

urlpatterns = [
    path('organizer-dashboard/', organizer_dashboard),
]