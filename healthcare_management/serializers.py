from rest_framework import serializers

from accounts.serializers import AccessTimesSerializer, ProfileSerializer
from dictili_medical.serializers import SymptomSerializer, PathologySerializer, SpecialitySerializer
from healthcare_management.models import HealthCareWorker, Patient, DiagnosticHistory, DiagnosisAction, HealthCare, \
    Service, Room, Furniture, Instrument


class HealthCareWorkerSerializer(serializers.ModelSerializer):
    access_time = AccessTimesSerializer(read_only=True)
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = HealthCareWorker
        fields = ['identifier', 'professional_card', 'works_at', 'access_time', 'profile', 'worker_type']


class PatientSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = Patient
        fields = ['profile', 'insurance_number']


class DiagnosisActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosisAction
        fields = ['name']


class DiagnosticHistorySerializer(serializers.ModelSerializer):
    by = HealthCareWorkerSerializer(read_only=True)
    patient = PatientSerializer(read_only=True)
    action = DiagnosisActionSerializer(read_only=True)
    symptoms = SymptomSerializer(read_only=True)
    diagnosed_with = PathologySerializer(read_only=True)

    class Meta:
        model = DiagnosticHistory
        fields = ['by', 'patient', 'action', 'comment', 'symptoms', 'diagnosed_with']


class HealthCareSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthCare
        fields = ['name', 'address', 'city', 'phone', 'type']


class ServiceSerializer(serializers.ModelSerializer):
    speciality = SpecialitySerializer(read_only=True)
    belongs_to = HealthCareSerializer(read_only=True)

    class Meta:
        model = Service
        fields = ['name', 'speciality', 'belongs_to']


class RoomSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = Room
        fields = ['number', 'service']


class FurnitureSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = Furniture
        fields = ['number', 'service', 'f_type']


class InstrumentSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = Instrument
        fields = ['number', 'service', 'i_type']
