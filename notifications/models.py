from django.db import models

from django.utils.translation import gettext_lazy as _

from base_backend.models import DeletableModel, do_nothing, cascade


class NotificationTopic(DeletableModel):
    topic_name = models.CharField(max_length=30, unique=True)


class Notification(DeletableModel):
    NOTIFICATIONS_TYPES = (('P', _('Personal')), ('T', _('TOPIC')), ('M', _('Multiple Users')))

    notification_type = models.CharField(choices=NOTIFICATIONS_TYPES, max_length=2)
    topic = models.ForeignKey('NotificationTopic', on_delete=do_nothing, related_name='notifications', null=True)
    sent = models.BooleanField(default=False)
    scheduled = models.BooleanField(default=False)
    send_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=150)
    message = models.CharField(max_length=300)


class NotificationToken(DeletableModel):
    user = models.OneToOneField('accounts.User', on_delete=cascade, related_name="notification_token")
    token = models.CharField(max_length=255, unique=True)


class NotificationHistory(DeletableModel):
    notification = models.ForeignKey('Notification', on_delete=cascade, related_name='receivers')
    user_token = models.ForeignKey('NotificationToken', on_delete=cascade, related_name='notifications')
    received = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
