from django.urls import path
from events.views import show_events

urlpatterns = [
    path('show-events/', show_events),
]