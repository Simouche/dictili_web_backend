from rest_framework import serializers

from notifications.models import Notification, NotificationHistory


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['notification_type', 'topic', 'sent', 'scheduled', 'send_at', 'title', 'message']


class NotificationHistorySerializer(serializers.ModelSerializer):
    notification = NotificationSerializer(read_only=True)

    class Meta:
        model = NotificationHistory
        fields = ['notification', 'received', 'read']
