from django.urls import path
from events.views import organizer_dashboard, create_event, update_event, delete_event, events_by_category,event_detail

urlpatterns = [
    path('organizer-dashboard/', organizer_dashboard, name="organizer-dashboard"),
    path('', events_by_category, name="events-by-category"),
    path('event-detail/<int:id>/', event_detail, name="event-detail"),
    path('create-event/', create_event, name="create-event"),
    path('update-event/<int:id>/', update_event, name="update-event"),
    path('delete-event/<int:id>/', delete_event, name="delete-event"),
    # path('view-events/', view_events),
]