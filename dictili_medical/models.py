from django.db import models

from django.utils.translation import gettext as _

from generic_backend.models import BaseModel
from localization_management.models import Country


class Medicine(BaseModel):
    lists = (('1', _('Liste I')), ('2', _('Liste II')), ('3', _('Liste III')))

    numero = models.IntegerField()
    numero_enregistrement = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=100)
    denomination_internationale = models.CharField(max_length=255)
    nom_marque = models.CharField(max_length=100)
    forme = models.CharField(max_length=30)
    dosage = models.CharField(max_length=50)
    cond = models.CharField(max_length=50, null=True)
    liste = models.CharField(max_length=10, choices=lists, null=True)
    p1 = models.ForeignKey('POneTwo', models.DO_NOTHING, related_name="pOne", null=True)
    p2 = models.ForeignKey('POneTwo', models.DO_NOTHING, related_name="pTwo", null=True)
    laboratoire_enregistrement = models.ForeignKey('MedicineLaboratory', models.DO_NOTHING, null=True)
    date_enregistrement_initial = models.DateField(null=True)
    date_enregistrement_final = models.DateField(null=True)
    type = models.ForeignKey('Type', models.DO_NOTHING, null=True)
    status = models.ForeignKey('Status', models.DO_NOTHING, null=True)
    duree_stabilite = models.IntegerField(null=True)

    @property
    def get_duree_stabilite(self):
        return str(self.duree_stabilite) + " " + _("MOIS")


class POneTwo(BaseModel):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name or 'OFF'


class MedicineLaboratory(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    country = models.ForeignKey(Country, models.DO_NOTHING)


class Type(BaseModel):
    name = models.CharField(max_length=20)


class Status(BaseModel):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

# Status.DoesNotExist