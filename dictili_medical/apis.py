from rest_framework.viewsets import ModelViewSet

from base_backend import permissions
from dictili_medical.models import MedicalDomain, Speciality, Pathology, Symptom
from dictili_medical.serializers import MedicalDomainSerializer, SpecialitySerializer, PathologySerializer, \
    SymptomSerializer


class MedicalDomainViewSet(ModelViewSet):
    serializer_class = MedicalDomainSerializer
    queryset = MedicalDomain.objects.all()
    permission_classes = [permissions.IsAdminOrReadOnly]


class SpecialityViewSet(ModelViewSet):
    serializer_class = SpecialitySerializer
    queryset = Speciality.objects.all()
    permission_classes = [permissions.IsAdminOrReadOnly]


class PathologyViewSet(ModelViewSet):
    serializer_class = PathologySerializer
    queryset = Pathology.objects.all()
    permission_classes = [permissions.IsAdminOrReadOnly]


class SymptomViewSet(ModelViewSet):
    serializer_class = SymptomSerializer
    queryset = Symptom.objects.all()
    permission_classes = [permissions.IsAdminOrReadOnly]
