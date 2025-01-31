from django.shortcuts import render
from django.db.models import Count
from django.utils.timezone import now
from django.http import HttpResponse
from events.forms import EventModelForm
from events.models import Event, Participant, Category

# Create your views here.

def home(request):
    # events = Event.objects.all()
    ps = Event.objects.prefetch_related('participants').all()
    events = Event.objects.annotate(participant_count=Count('participants'))
    return render(request, "home.html", {
        "events": events,
        'ps' : ps
        })

def organizer_dashboard(request):
    return render(request, "organizer-dashboard.html")

# def show_events(request):
#     return HttpResponse("Welcome to the event management system")


def create_event(request):
    # participants = Participant.objects.all()
    # categories = Category.objects.all()
    # form = EventModelForm(participants = participants, categories = categories)
    form = EventModelForm()

    if request.method == "POST":
        form = EventModelForm(request.POST)
        if form.is_valid():
            form.save()

            return render(request, "event_form.html", {"form": form, "message": "Event added successfully"})

    context = {"form": form}
    return render(request, "event_form.html", context)



def view_events(request):
    today = now().date()
    total_events = Event.objects.count()
    todays_event = Event.objects.filter(date=today)
    upcoming_events = Event.objects.filter(date__gte=today).count()
    past_events = Event.objects.filter(date__lt=today).count()
    all_participants = Participant.objects.all().count()

    return render(request, "show_events.html", {
        "todays_event": todays_event,
        'total_events': total_events,
        "upcoming_events": upcoming_events,
        "past_events": past_events,
        "all_participants": all_participants,
        }) 