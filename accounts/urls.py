from django.urls import path, include
from rest_framework.routers import SimpleRouter

from accounts import apis

api_router = SimpleRouter()
api_router.register('users', apis.UserViewSet, basename='users')
api_router.register('profiles', apis.ProfileViewSet, basename='profiles')
api_router.register('access-times', apis.AccessTimesViewSet, basename='access-times')

extra_urls = [
    path('login/', apis.LoginApi.as_view()),
    # path('otp/', apis.OtpApi.as_view()),
    # path('version/', apis.version),
]

urlpatterns = [
    # api urls
    path('api/', include(extra_urls + api_router.urls)),
]
