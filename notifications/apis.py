from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from notifications.models import Notification, NotificationHistory
from notifications.serializers import NotificationSerializer, NotificationHistorySerializer


class NotificationViewSet(ModelViewSet):
    serializer_class = NotificationSerializer
    queryset = Notification
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class NotificationHistoryViewSet(ModelViewSet):
    serializer_class = NotificationHistorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = NotificationHistory
