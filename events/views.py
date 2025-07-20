
from django.shortcuts import render, redirect
from django.db.models import Q, Count 
from django.utils.timezone import now, localdate
from django.http import HttpResponse
from events.forms import EventModelForm, CategoryModelForm 
from events.models import Event, Category, User 
from django.contrib import messages
from core.views import home
from users.views import is_admin
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import ContextMixin
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy


def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()

def is_participant(user):
    return user.groups.filter(name='User').exists()
 
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
    events = Event.objects.select_related('category').prefetch_related('participants').annotate(participant_count=Count('participants'))

    if search:
        events = events.filter(title__icontains=search) | events.filter(location__icontains=search)    
    context = {
        'events': events, 'search': search
        }
    return render(request, "show_events.html", context)

class ShowEvents(ListView):
    model = Event
    context_object_name = 'events'
    template_name = "show_events.html"

    def get_queryset(self):
        search = self.request.GET.get('search', '')
        queryset = Event.objects.select_related('category').prefetch_related('participants').annotate(participant_count=Count('participants'))
        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(location__icontains=search)) 
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        return context
    

@login_required
def event_detail(request, id):
    event = Event.objects.filter(id=id).select_related('category').prefetch_related('participants').annotate(participant_count=Count('participants'))
    
    context = {'event': event.first()}
    return render(request, "event_detail.html", context)

class EventDetail(LoginRequiredMixin, DetailView):
    model = Event
    template_name = "event_detail.html"
    context_object_name = 'event'
    pk_url_kwarg = 'id'

    def get_queryset(self):
        queryset = Event.objects.select_related('category').prefetch_related('participants').annotate(participant_count=Count('participants'))
        return queryset

@login_required
@permission_required("events.add_event", login_url='no-permission')
def create_event(request):

    if request.method == "POST":
        event_form = EventModelForm(request.POST, request.FILES)
        category_form = CategoryModelForm(request.POST)
        
        if "add_category" in request.POST and category_form.is_valid():
            category_form.save()
            messages.success(request, "Category added successfully!")
            return redirect("create-event")

        if "create_event" in request.POST and event_form.is_valid():
            event = event_form.save(commit=False)
            event.save()

            participants = event_form.cleaned_data.get("participants")
            event.participants.set(participants)

            messages.success(request, "Event added successfully!")
            return redirect("create-event")
        
    else:
        event_form = EventModelForm()
        category_form = CategoryModelForm()

    context = {
        "event_form": event_form,
        "category_form": category_form,
        "categories": Category.objects.all(),
        "participants": User.objects.filter(groups__name="User"), 
    }
    return render(request, "event_form.html", context)


class CreateEvent(ContextMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    template_name = "event_form.html"
    login_url = 'sign-in'	
    permission_required = "events.add_event"
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["event_form"] = kwargs.get('event_form', EventModelForm())
        context["category_form"] = kwargs.get('category_form', CategoryModelForm())
        context["categories"] = kwargs.get(Category.objects.all())
        context["participants"] = kwargs.get(User.objects.filter(groups__name="User"))
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        event_form = EventModelForm(request.POST, request.FILES)
        category_form = CategoryModelForm(request.POST)
        
        if "add_category" in request.POST and category_form.is_valid():
            category_form.save()
            messages.success(request, "Category added successfully!")
            return redirect('create-event')

        if "create_event" in request.POST and event_form.is_valid():
            event = event_form.save(commit=False)
            event.save()

            participants = event_form.cleaned_data.get("participants")
            event.participants.set(participants)

            messages.success(request, "Event added successfully!")
            return redirect("create-event")

@login_required
@permission_required("events.change_event", login_url='no-permission')
def update_event(request, id):
    event = Event.objects.get(id=id)
    event_form = EventModelForm(instance=event)
    category_form = CategoryModelForm()

    if request.method == "POST":
        event_form = EventModelForm(request.POST, instance=event)
        category_form = CategoryModelForm(request.POST)

        if event_form.is_valid():
            event_form.save()

            participants = event_form.cleaned_data.get("participants")
            if participants:
                event.participants.set(participants)

            messages.success(request, "Event updated successfully")
            return redirect('update-event', id)
        else:
            messages.error(request, "Please correct the errors below.")

    context = {"event_form": event_form, "category_form": category_form}
    return render(request, "event_form.html", context)


update_decorators = [login_required, permission_required("events.change_event", login_url='sign-in')]
@method_decorator(update_decorators, name="dispatch")
class UpdateEvent(UpdateView):
    model = Event
    pk_url_kwarg = 'id'
    form_class  = EventModelForm
    template_name = "event_form.html"
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)     
        context["event_form"] = self.get_form()
        context["category_form"] = CategoryModelForm
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        event_form = EventModelForm(request.POST, instance=self.object)

        if event_form.is_valid():
            event_form.save()

            participants = event_form.cleaned_data.get("participants")
            if participants:
                self.object.participants.set(participants)

            messages.success(request, "Event updated successfully")
            return redirect('update-event', self.object.id)
        return redirect('update-event', self.object.id)


@login_required
@permission_required("events.delete_event", login_url='no-permission')
def delete_event(request, id):
    if request.method =="POST":
        event = Event.objects.get(id=id)
        event.delete()
        messages.success(request, 'Event deleted successfully')
        return redirect('show-events')
    else:
        messages.success(request, 'Something went wrong')
        return redirect('show-events')

delete_decorators = [login_required, permission_required("events.delete_event", login_url='sign-in')]
@method_decorator(delete_decorators, name="dispatch")
class DeleteEvent(DeleteView):
    model = Event
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('show-events')

    def post(self, request, *args, **kwargs):
        deleteEvent = super().post(request, *args, **kwargs)
        messages.success(request, 'Event deleted successfully')
        return deleteEvent
    
    def get(self, request, *args, **kwargs):
        messages.error(request, 'Something went wrong')
        return redirect(self.success_url)


@user_passes_test(is_organizer, login_url='no-permission')
def organizer_dashboard(request):
    type = request.GET.get('type','all')
    
    today = now().date()
    todays_event = Event.objects.filter(date=today)
    all_participants = User.objects.filter(groups__name="User")  
    all_participants_count = all_participants.count()
    
    participant_events = []
    for participant in all_participants:
        next_event = participant.rsvp_events.filter(date__gte=now().date()).order_by('date').first()
        participant_events.append((participant, next_event))

    base_query = Event.objects.select_related('category').prefetch_related('participants')

    if type == 'all':
        events = base_query.all()
    elif type == 'upcoming events':
        events = base_query.filter(date__gte=today)
    elif type == 'past events':
        events = base_query.filter(date__lt=today)
    elif type == 'total events':
        events = base_query.all()
    elif type == 'all participants':
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
        'participant_events' : participant_events,
        'dashboard_url': 'organizer-dashboard',
        }
    return render(request, "organizer-dashboard.html", context)


@user_passes_test(is_participant)
def user_dashboard(request):
    type = request.GET.get('type','all')
    
    today = now().date()
    my_rsvp_events = request.user.rsvp_events.all()
    todays_event = Event.objects.filter(date=today)
    
    base_query = Event.objects.select_related('category').prefetch_related('participants')
    if type == 'all':
        events = my_rsvp_events
    elif type == 'total events':
        events = base_query.all()
    elif type == 'upcoming events':
        events = base_query.filter(date__gte=today)
    elif type == 'past events':
        events = base_query.filter(date__lt=today)
    elif type == 'past rsvp events': 
        events = my_rsvp_events.filter(date__lt=today)  

    counts = Event.objects.aggregate(
        total_events = Count('id'),
        upcoming_events_count = Count('id', filter= Q(date__gte=today)),
        past_events_count = Count('id', filter= Q(date__lt=today))
    )
    next_rsvp_events = my_rsvp_events.filter(date__gte=today)
    rsvp_counts = request.user.rsvp_events.aggregate(
        past_rsvp_events_count=Count('id', filter=Q(date__lt=today)),
    )
    context = {
        'events': events,
        'counts': counts,
        'type' : type.upper,
        "todays_event": todays_event,

        "rsvp_counts": rsvp_counts,
        "my_rsvp_events": my_rsvp_events,
        "next_rsvp_events": next_rsvp_events,
        'dashboard_url': 'user-dashboard',
        }
    return render(request, "user-dashboard.html", context)


@login_required
def rsvp_event(request, id):
    event = Event.objects.get(id=id)

    if request.user.groups.filter(name="User").exists():
        if request.user in event.participants.all():
            messages.info(request, "You already RSVP’d to this event.")
        else:
            event.participants.add(request.user)
            messages.success(request, "RSVP successful! Check your email for confirmation.")
    else:
        messages.warning(request, "Only participants can RSVP.")

    return redirect('event-detail', id=id)


@login_required
def dashboard(request):
    print("User:", request.user)
    print("Groups:", request.user.groups.all())
    
    if is_organizer(request.user):
        return redirect('organizer-dashboard')
    
    elif is_participant(request.user):
        return redirect('user-dashboard')
    
    elif is_admin(request.user):
        return redirect('admin-dashboard')

    return redirect('no-permission')
