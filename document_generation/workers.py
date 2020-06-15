import datetime
import io
import os
from threading import Thread

from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
from reportlab.pdfgen import canvas

from base_backend.text_utils import trim_text_to_90chars
from dictili.settings import MEDIA_ROOT, TEXT_ROOT_WORKER


class TranscriptionWorker(Thread):

    def __init__(self, *args, **kwargs):
        super(TranscriptionWorker, self).__init__(*args, **kwargs)

    def prepare(self, audio_path: str, language_code: str = "fr-FR",
                sample_rate_hertz: int = 8000, save_to: str = None, user_id: int = None) -> None:
        self.audio_path = audio_path
        self.language_code = language_code
        self.sammple_rate_herts = sample_rate_hertz
        self.save_to = save_to
        self.user_id = user_id

    def run(self) -> None:
        result_text = self.transcriber()
        path = self.pdf_maker(result_text, save_to=os.path.join(TEXT_ROOT_WORKER, "reports"))
        nlp_worker = NLPWorker()
        nlp_worker.prepare(result_text, 0, path, user_id=self.user_id)
        nlp_worker.start()

        print(path)
        print("transcripter finished")

    def transcriber(self) -> str:
        """
        Transcribe a short audio file using synchronous speech recognition

        Args:
          local_file_path Path to local audio file, e.g. /path/audio.wav
        """

        client = speech_v1.SpeechClient()

        # local_file_path = 'resources/brooklyn_bridge.raw'

        # The language of the supplied audio
        language_code = self.language_code

        # Sample rate in Hertz of the audio data sent
        sample_rate_hertz = self.sammple_rate_herts

        # Encoding of audio data sent. This sample sets this explicitly.
        # This field is optional for FLAC and WAV audio formats.
        encoding = enums.RecognitionConfig.AudioEncoding.AMR
        config = {
            "language_code": language_code,
            "sample_rate_hertz": sample_rate_hertz,
            "encoding": encoding,
        }
        with io.open(os.path.join(MEDIA_ROOT, self.audio_path), "rb") as f:
            content = f.read()
        audio = {"content": content}

        response = client.recognize(config, audio)
        return response.results[0].alternatives[0].transcript

    def pdf_maker(self, text: str, save_to: str = None) -> str:
        # TODO: make this more generic, for titles, text...etc
        file_name = "Test_at_" + datetime.datetime.now().__str__().replace(":", "_") + ".pdf"

        if save_to:
            file_path = os.path.join(save_to, file_name)
        else:
            file_path = os.path.join(TEXT_ROOT_WORKER, file_name)
        document_title = "Rapport"
        title = "Rapport Medicale"

        pdf = canvas.Canvas(file_path)
        pdf.setTitle(document_title)
        pdf.drawString(30, 800, "Doctor Full Name")
        pdf.drawString(30, 780, "Qualifications")
        pdf.drawString(30, 760, "Addresse")
        pdf.drawString(30, 740, "Position")
        pdf.drawString(30, 720, "Experience pour ce genre de cas")

        pdf.drawCentredString(300, 690, title)
        pdf.drawCentredString(300, 660, datetime.datetime.now().date().__str__())

        pdf.drawString(30, 630, "Rapport preparé pour")
        pdf.drawString(30, 610, "Full Name")
        pdf.drawString(30, 590, "Organisation")
        pdf.drawString(30, 570, "Addresse")

        pdf.line(30, 540, 550, 540)

        pdf.drawCentredString(300, 500, title)

        text_lines = trim_text_to_90chars(text)

        text = pdf.beginText(30, 450)
        for line in text_lines:
            text.textLine(line)
        pdf.drawText(text)

        pdf.drawString(400, 100, "Caché et Signature")
        pdf.save()
        return file_path


class NLPWorker(Thread):

    def prepare(self, text: str, audio_file: int, file_path: str, doc_type: str = 'P', user_id: int = None) -> None:
        self.text = text
        self.audio_file = audio_file
        self.file_path = file_path
        self.type = doc_type
        self.user_id = user_id

    def run(self) -> None:
        from document_generation.models import Document
        document = Document.objects.create(type=self.type, audio_file_id=self.audio_file, text=self.text,
                                           text_file=self.file_path)
        words, ids = self.context_checker()
        document.words.add(*ids)

        print("nlp worker finished")

    def context_checker(self) -> tuple:
        from healthcare_management.models import HealthCareWorker
        from document_generation.nlp_utils import pre_processing
        from document_generation.models import Word
        from document_generation.models import ContextScore
        from document_generation.models import OutOfContext

        domain = HealthCareWorker.objects.get(pk=self.user_id).works_at.speciality.domain
        processed_text = pre_processing(self.text)
        existing_words = Word.objects.all().values_list('word', flat=True)
        medical_words = [word for word in processed_text if word in existing_words]
        out_of_context = [word for word in processed_text if word not in existing_words]

        for word in medical_words:
            for another_word in medical_words:
                score, created = ContextScore.objects.get_or_create(word=word, another_word=another_word, domain=domain)
                if not created:
                    score.score += 1
                    score.save()

        for word in out_of_context:
            word, created = OutOfContext.objects.get_or_create(word=word)
            if not created:
                word.count += 1
                word.save()

        medical_words_ids = Word.objects.filter(word__in=medical_words).values_list('pk', flat=True)

        return medical_words, medical_words_ids
