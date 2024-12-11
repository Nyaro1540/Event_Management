from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import User, Event, Participant, Notification, Discussion
from datetime import datetime, timedelta

class EventManagementTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.organizer = User.objects.create_user(username='organizer', email='organizer@test.com', password='testpass', role='ORGANIZER')
        self.participant = User.objects.create_user(username='participant', email='participant@test.com', password='testpass', role='PARTICIPANT')
        self.client.force_authenticate(user=self.organizer)

    def test_create_event(self):
        data = {
            'title': 'Test Event',
            'description': 'This is a test event',
            'location': 'Test Location',
            'date': (datetime.now() + timedelta(days=1)).isoformat(),
            'capacity': 100,
            'schedule': 'Event schedule here'
        }
        response = self.client.post('/api/events/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(Event.objects.get().title, 'Test Event')

    def test_register_for_event(self):
        event = Event.objects.create(
            title='Event to Register',
            description='Register for this event',
            location='Register Location',
            date=datetime.now() + timedelta(days=1),
            capacity=25,
            schedule='Event schedule',
            creator=self.organizer
        )
        self.client.force_authenticate(user=self.participant)
        response = self.client.post(f'/api/users/{self.participant.id}/register/', {'event_id': event.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Participant.objects.count(), 1)

    def test_create_discussion(self):
        event = Event.objects.create(
            title='Discussion Event',
            description='Event with discussion',
            location='Discussion Location',
            date=datetime.now() + timedelta(days=1),
            capacity=25,
            schedule='Event schedule',
            creator=self.organizer
        )
        data = {
            'content': 'This is a test discussion message',
            'event': event.id
        }
        response = self.client.post('/api/discussions/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Discussion.objects.count(), 1)
        self.assertEqual(Discussion.objects.get().content, 'This is a test discussion message')

    def test_send_notification(self):
        event = Event.objects.create(
            title='Notification Event',
            description='Event with notification',
            location='Notification Location',
            date=datetime.now() + timedelta(days=1),
            capacity=25,
            schedule='Event schedule',
            creator=self.organizer
        )
        data = {
            'message': 'This is a test notification',
            'event': event.id,
            'recipient': self.participant.id
        }
        response = self.client.post('/api/notifications/send_notification/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Notification.objects.count(), 1)
        self.assertEqual(Notification.objects.get().message, 'This is a test notification')