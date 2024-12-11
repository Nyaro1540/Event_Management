from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from events.views import UserViewSet, EventViewSet, ParticipantViewSet, NotificationViewSet, DiscussionViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'events', EventViewSet)
router.register(r'participants', ParticipantViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'discussions', DiscussionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]