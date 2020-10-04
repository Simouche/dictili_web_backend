from rest_framework import serializers

from notifications.models import Notification, NotificationHistory, NotificationToken


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['notification_type', 'topic', 'sent', 'scheduled', 'send_at', 'title', 'message']


class NotificationHistorySerializer(serializers.ModelSerializer):
    notification = NotificationSerializer(read_only=True)

    class Meta:
        model = NotificationHistory
        fields = ['notification', 'received', 'read']


class NotificationTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationToken
        fields = ['user', 'token']
        extra_kwargs = {
            'user': {'write_only': True}
        }
