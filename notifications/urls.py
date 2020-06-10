from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import apis

router = SimpleRouter()
router.register('notifications', apis.NotificationViewSet, basename='notifications')
router.register('notifications-history', apis.NotificationHistoryViewSet, basename='notifications-history')

urlpatterns = [
    # api
    path('api/', include(router.urls))
]
