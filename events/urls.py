from django.urls import path
from events.views import organizer_dashboard, user_dashboard, create_event, CreateEvent, update_event, delete_event, events_by_category, event_detail, show_events, rsvp_event


urlpatterns = [
    path('', events_by_category, name="events-by-category"),
    path('show-events/', show_events, name="show-events"),
    path('event-detail/<int:id>/', event_detail, name="event-detail"),
    path('organizer-dashboard/', organizer_dashboard, name="organizer-dashboard"),
    path('user-dashboard/', user_dashboard, name="user-dashboard"),

    # path('create-event/', create_event, name="create-event"),
    path('create-event/', CreateEvent.as_view(), name="create-event"),
    path('update-event/<int:id>/', update_event, name="update-event"),
    path('delete-event/<int:id>/', delete_event, name="delete-event"),
    path('event-detail/<int:id>/rsvp/', rsvp_event, name="rsvp-event"),
]

