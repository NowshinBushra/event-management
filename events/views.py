
from django.shortcuts import render, redirect
from django.db.models import Q, Count 
from django.utils.timezone import now, localdate
from django.http import HttpResponse
from events.forms import EventModelForm
from events.models import Event, Participant, Category
from django.contrib import messages

# Create your views here.

def home(request):
    # events = Event.objects.all()
    ps = Event.objects.prefetch_related('participants').all()
    events = Event.objects.annotate(participant_count=Count('participants'))
    return render(request, "home.html", {
        "events": events,
        'ps' : ps
        })


# def show_events(request):
#     return HttpResponse("Welcome to the event management system")
 # participants = Participant.objects.all()
    # categories = Category.objects.all()
    # form = EventModelForm(participants = participants, categories = categories)

def create_event(request):
   
    form = EventModelForm()

    if request.method == "POST":
        form = EventModelForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.save()

            participants = form.cleaned_data.get('participants') 
            event.participants.set(participants)

            messages.success(request, "Event added successfully")
            return redirect('create-event')

    context = {"form": form}
    return render(request, "event_form.html", context)


def update_event(request, id):
    event = Event.objects.get(id=id)
    form = EventModelForm(instance=event)

    if request.method == "POST":
        form = EventModelForm(request.POST, instance=event)
        if form.is_valid():
            form.save()

            messages.success(request, "Event updated successfully")
            return redirect('update-event', id)

    context = {"form": form}
    return render(request, "event_form.html", context)

def delete_event(request, id):
    if request.method =="POST":
        event = Event.objects.get(id=id)
        event.delete()
        messages.success(request, 'Event deleted successfully')
        return redirect('organizer-dashboard')
    else:
        messages.success(request, 'Something went wrong')
        return redirect('organizer-dashboard')







def organizer_dashboard(request):
    type = request.GET.get('type','all')

    today = now().date()
    todays_event = Event.objects.filter(date=today)

    all_participants = Participant.objects.all()
    all_participants_count = all_participants.count()
    
    base_query = Event.objects.select_related('category').prefetch_related('participants')

    if type == 'all':
        events = base_query.all()
    elif type == 'upcoming events':
        events = base_query.filter(date__gte=today)
    elif type == 'past events':
        events = base_query.filter(date__lt=today)
    elif type == 'all_participants':
        events = all_participants

    

    counts = Event.objects.aggregate(
        total_events = Count('id'),
        upcoming_events_count = Count('id', filter= Q(date__gte=today)),
        past_events_count = Count('id', filter= Q(date__lt=today))
    )
    context = {
        'events': events,
        'counts': counts,
        'type' : type.upper,
        "todays_event": todays_event,
        "all_participants": all_participants,
        "all_participants_count": all_participants_count,
        }

    return render(request, "organizer-dashboard.html", context)


# def view_events(request):
#     today = now().date()
#     total_events = Event.objects.count()
#     todays_event = Event.objects.filter(date=today)

#     upcoming_events = Event.objects.filter(date__gte=today)
#     upcoming_events_count = upcoming_events.count()

#     past_events = Event.objects.filter(date__lt=today)
#     past_events_count = past_events.count()

#     all_participants = Participant.objects.all()
#     all_participants_count = all_participants.count()

#     context = {
#         "todays_event": todays_event,
#         'total_events': total_events,

#         "upcoming_events": upcoming_events,
#         "upcoming_events_count": upcoming_events_count,
#         "past_events": past_events,
#         "past_events_count": past_events_count,
#         "all_participants": all_participants,
#         "all_participants_count": all_participants_count,
#         }

#     return render(request, "organizer-dashboard.html", context) 