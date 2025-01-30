from django.shortcuts import render
from django.utils.timezone import now
from django.http import HttpResponse
from events.forms import EventModelForm
from events.models import Event, Participant, Category

# Create your views here.

def home(request):
    return render(request, "home.html")

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
    all_events = Event.objects.all()
    todays_event = Event.objects.filter(date=today)
    upcoming_event = Event.objects.filter(date__gte=today)
    past_event = Event.objects.filter(date__lt=today)
    return render(request, "show_events.html", {
        "all_events": all_events,
        "todays_event": todays_event,
        "upcoming_event": upcoming_event,
        "past_event": past_event,
        }) 