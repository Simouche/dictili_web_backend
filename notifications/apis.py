from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from notifications.models import Notification, NotificationHistory, NotificationToken
from notifications.serializers import NotificationSerializer, NotificationHistorySerializer, NotificationTokenSerializer


class NotificationViewSet(ModelViewSet):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class NotificationHistoryViewSet(ModelViewSet):
    serializer_class = NotificationHistorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = NotificationHistory.objects.all()


class NotificationTokenViewSet(ModelViewSet):
    serializer_class = NotificationTokenSerializer
    permissions = [permissions.IsAuthenticatedOrReadOnly]
    queryset = NotificationToken.objects.all()

    def create(self, request, *args, **kwargs):
        obj = request.data.copy()
        obj['user'] = request.user.pk
        obj.data = obj
        return super(NotificationTokenViewSet, self).create(obj, *args, **kwargs)
