import glob
import os

from django.db.models.signals import post_save
from django.dispatch import receiver

from base_backend.models import do_nothing
from dictili.settings import TEXT_ROOT, AUDIO_ROOT, TEXT_ROOT_WORKER
from generic_backend.models import BaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class Word(BaseModel):
    word = models.CharField(max_length=255, unique=True, null=False)
    contexts = models.ManyToManyField("self", through='ContextScore', through_fields=('word', 'another_word'))


class ContextScore(BaseModel):
    word = models.ForeignKey('Word', on_delete=do_nothing, related_name="first_context")
    another_word = models.ForeignKey('Word', on_delete=do_nothing, related_name="second_context")
    domain = models.ForeignKey("dictili_medical.MedicalDomain", on_delete=do_nothing, related_name="contexts")
    score = models.IntegerField(default=0)

    class Meta:
        unique_together = ('word', 'another_word', 'domain')


class OutOfContext(BaseModel):
    word = models.CharField(max_length=255, unique=True, null=False)
    count = models.IntegerField(default=0)


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


@receiver(post_save, sender=AudioFile)
def audio_file_created_signal(sender, instance, created, raw, **kwargs):
    if created and not raw:
        from document_generation.workers import TranscriptionWorker
        transcription_worker = TranscriptionWorker()
        transcription_worker.prepare(instance.file_location.path)
        transcription_worker.start()
