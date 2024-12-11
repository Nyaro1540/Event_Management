from django.forms import ValidationError
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Event, Participant, Notification, Discussion
from .serializers import UserSerializer, EventSerializer, ParticipantSerializer, NotificationSerializer, DiscussionSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['post'])
    def register(self, request, pk=None):
        user = self.get_object()
        event_id = request.data.get('event_id')
        try:
            event = Event.objects.get(id=event_id)
            user.register(event)
            return Response({'status': 'registered'})
        except Event.DoesNotExist:
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def unregister(self, request, pk=None):
        user = self.get_object()
        event_id = request.data.get('event_id')
        try:
            event = Event.objects.get(id=event_id)
            user.unregister(event)
            return Response({'status': 'unregistered'})
        except Event.DoesNotExist:
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def perform_update(self, serializer):
        serializer.save()
        serializer.instance.notify_changes()

    @action(detail=True, methods=['post'])
    def notify_changes(self, request, pk=None):
        event = self.get_object()
        event.notify_changes()
        return Response({'status': 'notifications sent'})

class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    @action(detail=False, methods=['post'])
    def send_notification(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        Notification.send_notification(**serializer.validated_data)
        return Response({'status': 'notification sent'})

    @action(detail=False, methods=['post'])
    def schedule_reminder(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        Notification.schedule_reminder(**serializer.validated_data)
        return Response({'status': 'reminder scheduled'})

class DiscussionViewSet(viewsets.ModelViewSet):
    queryset = Discussion.objects.all()
    serializer_class = DiscussionSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def moderate(self, request, pk=None):
        discussion = self.get_object()
        discussion.moderate_message()
        return Response({'status': 'message moderated'})