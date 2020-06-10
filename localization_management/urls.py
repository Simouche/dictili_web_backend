from django.urls import include, path
from rest_framework.routers import SimpleRouter
from . import apis

router = SimpleRouter()
router.register('countries', apis.CountryViewSet, basename='countries')
router.register('states', apis.StateViewSet, basename='states')
router.register('cities', apis.CityViewSet, basename='cities')

urlpatterns = [
    # apis
    path('api/', include(router.urls))
]
