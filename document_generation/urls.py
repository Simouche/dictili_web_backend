from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import apis

router = SimpleRouter()
router.register("audio-file", apis.AudioFileViewSet, basename="audio-files")

urlpatterns = [
    path('api/', include(router.urls))
]
