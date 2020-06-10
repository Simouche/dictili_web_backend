from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from base_backend import permissions as mperms
from healthcare_management.models import HealthCareWorker, Patient, DiagnosisAction, HealthCare, Service, Room, \
    Furniture, Instrument
from healthcare_management.serializers import HealthCareWorkerSerializer, PatientSerializer, DiagnosisActionSerializer, \
    HealthCareSerializer, ServiceSerializer, RoomSerializer, FurnitureSerializer, InstrumentSerializer


class HealthCareWorkerViewSet(ModelViewSet):
    serializer_class = HealthCareWorkerSerializer
    queryset = HealthCareWorker.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PatientViewSet(ModelViewSet):
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class DiagnosisActionViewSet(ModelViewSet):
    serializer_class = DiagnosisActionSerializer
    queryset = DiagnosisAction
    permission_classes = [mperms.IsAdminOrReadOnly]


class HealthCareViewSet(ModelViewSet):
    serializer_class = HealthCareSerializer
    permission_classes = [mperms.IsAdminOrReadOnly]
    queryset = HealthCare.objects.all()


class ServiceViewSet(ModelViewSet):
    permission_classes = [mperms.IsAdminOrReadOnly]
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()


class RoomViewSet(ModelViewSet):
    serializer_class = RoomSerializer
    permission_classes = [mperms.IsAdminOrReadOnly]
    queryset = Room.objects.all()


class FurnitureViewSet(ModelViewSet):
    serializer_class = FurnitureSerializer
    queryset = Furniture
    permission_classes = [mperms.IsAdminOrReadOnly]


class InstrumentViewSet(ModelViewSet):
    serializer_class = InstrumentSerializer
    queryset = Instrument
    permission_classes = [mperms.IsAdminOrReadOnly]
