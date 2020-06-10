from rest_framework import serializers

from dictili_medical.models import MedicalDomain, Speciality, Pathology, Symptom


class MedicalDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalDomain
        fields = ['name']


class SpecialitySerializer(serializers.ModelSerializer):
    domain = MedicalDomainSerializer()

    class Meta:
        model = Speciality
        fields = ['name', 'domain']


class PathologySerializer(serializers.ModelSerializer):
    speciality = SpecialitySerializer()

    class Meta:
        model = Pathology
        fields = ['name', 'speciality']


class SymptomSerializer(serializers.ModelSerializer):
    pathology = PathologySerializer()

    class Meta:
        model = Symptom
        fields = ['name', 'pathology']
