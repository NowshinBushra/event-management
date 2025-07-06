from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from events.models import Event
from django.contrib.auth.models import User
from django.conf import settings


@receiver(m2m_changed, sender=Event.participants.through)
def notify_participants_on_event_creation(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        assigned_participants = User.objects.filter(pk__in=pk_set)

        print(instance, instance.participants.all()) 
        print("Participants Emails:", assigned_participants) 
        for user in assigned_participants:
            send_mail(
                subject="RSVP Confirmation",
                message=f"You have been assigned to the event: {instance.title}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False
            )