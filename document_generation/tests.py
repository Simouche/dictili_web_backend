from django.test import TestCase

# Create your tests here.
from document_generation.models import Document, AudioFile


class DocumentAndWordTestCase(TestCase):
    def setUp(self) -> None:
        self.document = Document.objects.count(type='R', audio_file=AudioFile.objects.create())
