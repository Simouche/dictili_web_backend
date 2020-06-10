from rest_framework.viewsets import ModelViewSet

from base_backend import permissions
from localization_management.models import Country, State, City
from localization_management.serializers import CountrySerializer, StateSerializer, CitySerializer


class CountryViewSet(ModelViewSet):
    serializer_class = CountrySerializer
    permission_classes = [permissions.IsAdminOrReadOnly]
    queryset = Country.objects.all()


class StateViewSet(ModelViewSet):
    permission_classes = [permissions.IsAdminOrReadOnly]
    serializer_class = StateSerializer
    queryset = State.objects.all()


class CityViewSet(ModelViewSet):
    serializer_class = CitySerializer
    queryset = City.objects.all()
    permission_classes = [permissions.IsAdminOrReadOnly]
