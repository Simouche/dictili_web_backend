from django.db import models
from django.utils.translation import gettext_lazy as _

from base_backend.models import do_nothing, cascade
from generic_backend.models import BaseModel


class HealthCareWorker(BaseModel):
    WORKER_TYPE = (('N', _('Nurse')),
                   ('C', _('Caregiver')),
                   ('A', _('Anesthesist')),
                   ('D', _('Doctor')),
                   ('R', _('Resident')))

    identifier = models.CharField(max_length=255, unique=True)
    professional_card = models.ImageField(upload_to="media/cards")
    works_at = models.ForeignKey('healthcare_management.Service', on_delete=do_nothing, related_name="workers")
    access_time = models.ForeignKey('accounts.AccessTimes', on_delete=do_nothing, related_name="users")
    profile = models.OneToOneField('accounts.Profile', on_delete=cascade)
    worker_type = models.CharField(max_length=2, choices=WORKER_TYPE)


class Patient(BaseModel):
    profile = models.OneToOneField('accounts.Profile', on_delete=cascade)
    insurance_number = models.CharField(max_length=255, unique=True)


class DiagnosticHistory(BaseModel):
    by = models.ForeignKey('HealthCareWorker', on_delete=do_nothing, related_name="patients_history")
    patient = models.ForeignKey('Patient', on_delete=do_nothing, related_name="diagnosis_history")
    action = models.ForeignKey('DiagnosisAction', on_delete=do_nothing, related_name="diagnoses")
    comment = models.TextField()
    symptoms = models.ManyToManyField("dictili_medical.Symptom")
    diagnosed_with = models.ForeignKey('dictili_medical.Pathology', on_delete=do_nothing)


class DiagnosisAction(BaseModel):
    name = models.CharField(max_length=255, unique=True)


class HealthCare(BaseModel):
    TYPES = (('H', _('Hospital')), ('C', _('Clinic')), ('L', _('Laboratory')), ('R', _('Radio Center')))

    name = models.CharField(max_length=150)
    address = models.CharField(max_length=150, blank=True, null=True)
    city = models.ForeignKey('localization_management.City', on_delete=models.DO_NOTHING, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    Type = models.CharField(max_length=3, choices=TYPES)

    def __str__(self):
        return self.name


class Service(BaseModel):
    name = models.CharField(max_length=255)
    speciality = models.ForeignKey('dictili_medical.Speciality', on_delete=do_nothing, related_name="services")
    belongs_to = models.ForeignKey('HealthCare', on_delete=cascade, related_name="services")


class Equipment(BaseModel):
    number = models.IntegerField()
    service = models.ForeignKey("Service", on_delete=cascade)

    class Meta:
        abstract = True


class Room(Equipment):
    pass


class Furniture(Equipment):
    FURNITURE_TYPES = (('T', _('Table')), ('C', _('Chair')), ('B', _('Bed')))

    f_type = models.CharField(max_length=3, choices=FURNITURE_TYPES)


class Instrument(Equipment):
    INSTRUMENT_TYPES = (('B', _('Bistouri')), ('C', _('Cisors')))

    i_type = models.CharField(max_length=3, choices=INSTRUMENT_TYPES, null=True)
