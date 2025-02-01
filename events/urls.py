from django.urls import path
from events.views import organizer_dashboard, create_event, update_event

urlpatterns = [
    path('organizer-dashboard/', organizer_dashboard, name="organizer-dashboard"),
    path('create-event/', create_event, name="create-event"),
    path('update-event/<int:id>/', update_event, name="update-event"),
    # path('view-events/', view_events),
]