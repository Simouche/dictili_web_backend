import glob
import os

from base_backend.models import do_nothing
from dictili.settings import TEXT_ROOT, AUDIO_ROOT, TEXT_ROOT_WORKER
from generic_backend.models import BaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class Word(BaseModel):
    word = models.CharField(max_length=255, unique=True, null=False)
    context = models.ManyToManyField("self")
    domain = models.ManyToManyField("dictili_medical.MedicalDomain")


class Document(BaseModel):
    TYPES = (('p', _('Prescription')), ('r', _('Report')))

    type = models.CharField(max_length=3, choices=TYPES)
    words = models.ManyToManyField(Word)
    text = models.CharField(max_length=2048)
    text_file = models.FileField(upload_to=os.path.join(TEXT_ROOT, "prescription" if type == 'p' else 'reports'))
    audio_file = models.OneToOneField("document_generation.AudioFile", on_delete=do_nothing)

    @staticmethod
    def get_latest() -> str:
        files = glob.glob(os.path.join(TEXT_ROOT_WORKER, "reports", "*.pdf"))
        latest_file = max(files, key=os.path.getctime)
        return latest_file


class AudioFile(BaseModel):
    generated_by = models.OneToOneField("healthcare_management.HealthCareWorker", models.DO_NOTHING)
    concerns = models.OneToOneField("healthcare_management.Patient", do_nothing)
    file_location = models.FileField(upload_to=AUDIO_ROOT)
