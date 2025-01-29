from django.shortcuts import render
from django.http import HttpResponse
from events.forms import EventForm
from events.models import Participant, Category

# Create your views here.

def home(request):
    return render(request, "home.html")

def organizer_dashboard(request):
    return render(request, "organizer-dashboard.html")

# def show_events(request):
#     return HttpResponse("Welcome to the event management system")


def create_event(request):
    participants = Participant.objects.all()
    categories = Category.objects.all()
    form = EventForm(participants = participants, categories = categories)

    if request.method == "POST":
        form = EventForm(request.POST, participants = participants, categories = categories)
    context = {"form": form}
    return render(request, "event_form.html", context)
