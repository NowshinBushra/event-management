from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="events")
    participants = models.ManyToManyField(User, related_name="rsvp_events", blank=True)
    # participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="rsvp_events", blank=True)
    asset = models.ImageField(upload_to='event_asset', blank=True, null=True, default="event_asset/default_img.png")

    def __str__(self):
        return self.title
