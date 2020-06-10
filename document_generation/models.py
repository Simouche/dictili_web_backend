import os

from dictili.settings import TEXT_ROOT, AUDIO_ROOT, TEXT_ROOT_WORKER
from generic_backend.models import BaseModel
from django.db import models
from django.utils.translation import gettext as _

types = (('p', _('Prescription')), ('r', _('Report')))


class Word(BaseModel):
    word = models.CharField(max_length=255, unique=True, null=False)
    context = models.ManyToManyField("self", blank=True)
    # domain = models.ManyToManyField("todo")  # TODO: add specialities
    pass


class Document(BaseModel):
    type = models.CharField(max_length=3, choices=types)
    words = models.ManyToManyField(Word)
    text = models.CharField(max_length=2048)
    text_file = models.FileField(upload_to=os.path.join(TEXT_ROOT, "prescription" if type == 'p' else 'reports'))
    audio_file = models.OneToOneField("document_generation.AudioFile", on_delete=models.DO_NOTHING)

    @staticmethod
    def get_latest() -> str:
        files = os.listdir(os.path.join(TEXT_ROOT_WORKER, "reports"))
        file_path = os.path.join(TEXT_ROOT_WORKER, 'reports', files[-1])
        return file_path


class AudioFile(BaseModel):
    # generated_by = models.OneToOneField("healthcare_management.HealthCareWorker", models.DO_NOTHING)
    # concerns = models.OneToOneField("healthcare_management.Patient", models.DO_NOTHING)
    file_location = models.FileField(upload_to=AUDIO_ROOT)
