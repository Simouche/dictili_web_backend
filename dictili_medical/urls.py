from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import apis

router = SimpleRouter()
router.register('medical-domains', apis.MedicalDomainViewSet, basename="medical-domain")
router.register('specialities', apis.SpecialityViewSet, basename="speciality")
router.register('pathologies', apis.PathologyViewSet, basename="pathology")
router.register('symptoms', apis.SymptomViewSet, basename="symptom")

urlpatterns = [

    # api urls
    path('api/', include(router.urls))
]


