from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

class User(AbstractUser):
    ROLE_CHOICES = [
        ('ORGANIZER', 'Organisateur'),
        ('PARTICIPANT', 'Participant'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def register(self, event):
        if self.role == 'PARTICIPANT':
            Participant.objects.create(user=self, event=event, status='PENDING')
        else:
            raise ValidationError("Only participants can register for events.")

    def unregister(self, event):
        if self.role == 'PARTICIPANT':
            Participant.objects.filter(user=self, event=event).delete()
        else:
            raise ValidationError("Only participants can unregister from events.")

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date = models.DateTimeField()
    capacity = models.PositiveIntegerField()
    schedule = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')

    @classmethod
    def add_event(cls, **kwargs):
        return cls.objects.create(**kwargs)

    def edit_event(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()

    def delete_event(self):
        self.delete()

    def notify_changes(self):
        participants = Participant.objects.filter(event=self)
        for participant in participants:
            Notification.objects.create(
                message=f"Event '{self.title}' has been updated.",
                event=self,
                recipient=participant.user
            )

class Participant(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('APPROVED', 'Approuvé'),
        ('REJECTED', 'Refusé'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

class Notification(models.Model):
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)

    @classmethod
    def send_notification(cls, message, event, recipient):
        return cls.objects.create(message=message, event=event, recipient=recipient)

    @classmethod
    def schedule_reminder(cls, event, recipient, scheduled_time):
        # This method would typically use a task queue like Celery
        # For simplicity, we'll just create a notification
        cls.objects.create(
            message=f"Reminder: Event '{event.title}' is coming up!",
            event=event,
            recipient=recipient
        )

class Discussion(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    @classmethod
    def add_message(cls, content, author, event):
        return cls.objects.create(content=content, author=author, event=event)

    def moderate_message(self):
        # Implement moderation logic here
        pass

# Note: UIManager is not implemented as it's typically handled on the frontend