from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from events.models import Event


@receiver(m2m_changed, sender=Event.participants.through)
def notify_participants_on_event_creation(sender, instance, action, **kwargs):
    if action == "post_add":
        assigned_emails = [ptc.email for ptc in instance.participants.all()]

        print(instance, instance.participants.all()) 
        print("Participants Emails:", assigned_emails) 
        send_mail(
            "New event assigned",
            f"You have been assigned to the event: {instance.title}",
            "atiya.esha94@gmail.com",
            assigned_emails,
            fail_silently=False
        )