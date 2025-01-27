from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, "home.html")

def organizer_dashboard(request):
    return render(request, "organizer-dashboard.html")

# def show_events(request):
#     return HttpResponse("Welcome to the event management system")