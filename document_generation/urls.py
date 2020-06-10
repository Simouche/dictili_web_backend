from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import apis

router = SimpleRouter()
router.register("audio-file", apis.AudioFileViewSet, basename="audio-files")
router.register("text-file", apis.DocumentViewSet, basename="text-files")
router.register("words", apis.WordViewSet, basename="words")

urlpatterns = [
    path('api/', include(router.urls))
]
