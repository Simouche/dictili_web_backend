from rest_framework import serializers

from localization_management.models import Country, State, City


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['name', 'code', 'latitude', 'longitude']


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['name', 'matricule', 'code_postal', 'country', 'latitude', 'longitude']


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['name', 'code_postal', 'wilaya', 'latitude', 'longitude']
