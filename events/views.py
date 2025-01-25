from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return HttpResponse("Welcome to the event management system")

def show_events(request):
    return HttpResponse("Welcome to the event management system")