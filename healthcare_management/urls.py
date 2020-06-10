from django.urls import include, path
from rest_framework.routers import SimpleRouter
from . import apis

router = SimpleRouter()
router.register('employees', apis.HealthCareWorkerViewSet, basename="employees")
router.register('patients', apis.PatientViewSet, basename="patients")
router.register('diagnosis-actions', apis.DiagnosisActionViewSet, basename="diagnoses")
router.register('establishments', apis.HealthCareViewSet, basename="establishments")
router.register('services', apis.ServiceViewSet, basename="services")
router.register('rooms', apis.RoomViewSet, basename="rooms")
router.register('furnitures', apis.FurnitureViewSet, basename="furnitures")
router.register('instruments', apis.InstrumentViewSet, basename="instruments")

urlpatterns = [
    # api
    path('api/', include(router.urls))
]
