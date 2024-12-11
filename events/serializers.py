from rest_framework import serializers
from .models import User, Event, Participant, Notification, Discussion

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']

class EventSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'location', 'date', 'capacity', 'schedule', 'creator']

class ParticipantSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    event = EventSerializer(read_only=True)

    class Meta:
        model = Participant
        fields = ['id', 'status', 'user', 'event']

class NotificationSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'message', 'timestamp', 'event', 'recipient']

class DiscussionSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    event = EventSerializer(read_only=True)

    class Meta:
        model = Discussion
        fields = ['id', 'content', 'timestamp', 'author', 'event']