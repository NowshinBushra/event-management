
from django.shortcuts import render, redirect
from django.db.models import Q, Count 
from django.utils.timezone import now, localdate
from django.http import HttpResponse
from events.forms import EventModelForm, CategoryModelForm, ParticipantModelForm
from events.models import Event, Participant, Category
from django.contrib import messages
from core.views import home


def events_by_category(request):
    c_id = request.GET.get('category')
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    events = Event.objects.select_related('category').prefetch_related('participants').annotate(participant_count=Count('participants'))
    if c_id:
        events = events.filter(category_id=c_id)
    
    if start_date and end_date:
        events = events.filter(date__range=[start_date, end_date])

    context = {
        'events': events
        }
    return render(request, "home.html", context)



def show_events(request):
    search = request.GET.get('search', '')
    # print(search)
    events = Event.objects.select_related('category').prefetch_related('participants').annotate(participant_count=Count('participants'))

    if search:
        events = events.filter(title__icontains=search) | events.filter(location__icontains=search)
    
    context = {
        'events': events, 'search': search
        }
    return render(request, "show_events.html", context)


def event_detail(request, id):

    event = Event.objects.filter(id=id).select_related('category').prefetch_related('participants').annotate(participant_count=Count('participants'))
    
    context = {'event': event.first()}
    return render(request, "event_detail.html", context)
    


# def create_event(request): 
#     form = EventModelForm()

#     if request.method == "POST":
#         form = EventModelForm(request.POST)
#         if form.is_valid():
#             event = form.save(commit=False)
#             event.save()

#             participants = form.cleaned_data.get('participants') 
#             event.participants.set(participants)

#             messages.success(request, "Event added successfully")
#             return redirect('create-event')
#         else:
#             messages.error(request, "Please correct the errors below.")

#     context = {"form": form}
#     return render(request, "event_form.html", context)

# 

def create_event(request):
    event_form = EventModelForm()
    category_form = CategoryModelForm()
    participant_form = ParticipantModelForm()

    if request.method == "POST":
        event_form = EventModelForm(request.POST)
        category_form = CategoryModelForm(request.POST)
        participant_form = ParticipantModelForm(request.POST)
        
        if "add_category" in request.POST and category_form.is_valid():
            category_form.save()
            messages.success(request, "Category added successfully!")
            return redirect("create-event")

        if "add_participant" in request.POST and participant_form.is_valid():
            participant_form.save()
            messages.success(request, "Participant added successfully!")
            return redirect("create-event")

        if "create_event" in request.POST and event_form.is_valid():
            event = event_form.save(commit=False)
            event.save()

            participants = event_form.cleaned_data.get("participants")
            event.participants.set(participants)

            messages.success(request, "Event added successfully!")
            return redirect("create-event")

    context = {
        "event_form": event_form,
        "category_form": category_form,
        "participant_form": participant_form,
        "categories": Category.objects.all(),
        "participants": Participant.objects.all(),
    }
    return render(request, "event_form.html", context)


def update_event(request, id):
    event = Event.objects.get(id=id)
    event_form = EventModelForm(instance=event)
    category_form = CategoryModelForm()
    participant_form = ParticipantModelForm()

    if request.method == "POST":
        event_form = EventModelForm(request.POST, instance=event)
        category_form = CategoryModelForm(request.POST)
        participant_form = ParticipantModelForm(request.POST)

        if event_form.is_valid():
            event_form.save()

            participants = event_form.cleaned_data.get("participants")
            if participants:
                event.participants.set(participants)


            messages.success(request, "Event updated successfully")
            return redirect('update-event', id)
        else:
            messages.error(request, "Please correct the errors below.")

    context = {"event_form": event_form, "category_form": category_form, "participant_form": participant_form}
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
    print(type)

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
    elif type == 'total events':
        events = base_query.all()
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

