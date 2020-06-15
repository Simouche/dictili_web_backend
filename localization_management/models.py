from django.db import models

# Create your models here.
from base_backend.models import cascade
from generic_backend.models import BaseModel


class Country(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    def __str__(self):
        return self.name


class State(BaseModel):
    name = models.CharField(max_length=255)
    matricule = models.IntegerField()
    code_postal = models.IntegerField()
    country = models.ForeignKey('Country', on_delete=cascade, related_name="states")
    latitude = models.CharField(max_length=50, null=True)
    longitude = models.CharField(max_length=50, null=True)

    def __str__(self):
        return "{0} {1}".format(self.matricule, self.name)


class City(BaseModel):
    name = models.CharField(max_length=255)
    code_postal = models.IntegerField()
    wilaya = models.ForeignKey('State', on_delete=models.DO_NOTHING, related_name='cities')
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Cities"
