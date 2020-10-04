import datetime
import io
import json
import os
from queue import Queue
from threading import Thread

import pandas as pd
from django.db.models import QuerySet, Q
from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
from reportlab.pdfgen import canvas

from base_backend.text_utils import trim_text_to_90chars
from dictili.settings import TEXT_ROOT_WORKER
from document_generation import nlp_queue, inference_1_queue
from document_generation.nlp_utils import pre_processing


class TranscriptionWorker(Thread):
    transcription_queue = Queue()

    def __init__(self, *args, **kwargs):
        """

        :param queue: object of type Queue, will contain data for the transcription process
                        i.e: {'audio_file': 'AudioFileObject', 'save_to':'path', 'language_code':'fr-FR',
                        'sample_rate_hertz':8000}
        :param args:
        :param kwargs:
        """
        super(TranscriptionWorker, self).__init__(*args, **kwargs)

    def prepare(self, meta_data: dict) -> None:
        self.audio_file = meta_data.get('audio_file')
        self.language_code = meta_data.get('language_code', 'fr-FR')
        self.sample_rate_herts = meta_data.get('sample_rate_hertz', 8000)
        self.save_to = meta_data.get('save_to')
        self.user = self.audio_file.generated_by
        self.patient = self.audio_file.concerns

    def run(self) -> None:
        while True:
            meta_data = TranscriptionWorker.transcription_queue.get()
            self.prepare(meta_data=meta_data)
            result_text = self.transcriber()
            path = self.pdf_maker(result_text, save_to=self.save_to)
            nlp_data = {
                'text': result_text,
                'audio_file': self.audio_file,
                'file_path': path
            }
            inference_data = {
                'text': result_text,
                'patient': self.patient,
                'doctor': self.user
            }
            nlp_queue.put(nlp_data)  #
            inference_1_queue.put(inference_data)
            TranscriptionWorker.transcription_queue.task_done()

    def transcriber(self) -> str:
        """
        Transcribe a short audio file using asynchronous speech recognition

        Args:
          local_file_path Path to local audio file, e.g. /path/audio.wav
        """
        client = speech_v1.SpeechClient()
        language_code = self.language_code

        # Sample rate in Hertz of the audio data sent
        sample_rate_hertz = self.sample_rate_herts

        # Encoding of audio data sent. This sample sets this explicitly.
        # This field is optional for FLAC and WAV audio formats.
        encoding = enums.RecognitionConfig.AudioEncoding.AMR
        config = {
            "language_code": language_code,
            "sample_rate_hertz": sample_rate_hertz,
            "encoding": encoding,
        }
        with io.open(self.audio_file.file_location.path, "rb") as f:
            content = f.read()
        audio = {"content": content}
        # response = client.recognize(config, audio) this is for the short files
        operation = client.long_running_recognize(config, audio)
        response = operation.result()
        content = [result.alternatives[0].transcript for result in response.results]
        return "".join(content)

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
    """
    This worker is responsible for updating the domain context knowledge base.
    """

    def __init__(self, queue: Queue = None, *args, **kwargs):
        super(NLPWorker, self).__init__(*args, **kwargs)
        self.queue = queue

    def prepare(self, nlp_data: dict) -> None:
        self.text = nlp_data.get('text')
        self.audio_file = nlp_data.get('audio_file')
        self.file_path = nlp_data.get('file_path')
        self.type = nlp_data.get('doc_type', 'R')
        self.user = self.audio_file.generated_by

    def run(self) -> None:
        while True:
            nlp_data = self.queue.get()
            self.prepare(nlp_data)
            words, ids = self.context_checker()
            self.document_generator(ids)
            self.queue.task_done()

    def document_generator(self, ids: list) -> None:
        """
        save the document with its related words into the database, for later use.
        :param ids:
        :return: None
        """
        from document_generation.models import Document
        document = Document.objects.create(type=self.type, audio_file=self.audio_file, text=self.text,
                                           text_file="generated" + self.file_path.split('\\generated')[1])
        document.words.add(*ids)

    def context_checker(self) -> tuple:
        """
        checks to which context/domain the documents belongs, flags the out of context words and it creates relations
        between words to have bi-gram context.
        :return: tuple of words and their ids.
        """
        from document_generation.models import Word
        from document_generation.models import ContextScore
        from document_generation.models import OutOfContext

        domain = self.user.works_at.speciality.domain
        processed_text = pre_processing(self.text)
        existing_words = Word.objects.all().values_list('word', flat=True)
        medical_words = [word for word in processed_text if word in existing_words]
        out_of_context = [word for word in processed_text if word not in existing_words]

        for word in medical_words:
            for another_word in medical_words:
                if word != another_word:
                    score, created = ContextScore.objects.get_or_create(word=word, another_word=another_word,
                                                                        domain=domain)
                    if not created:
                        score.score += 1
                        score.save()

        for word in out_of_context:
            word, created = OutOfContext.objects.get_or_create(word=word)
            if not created:
                word.count += 1
                word.save()

        medical_words_records = Word.objects.filter(word__in=medical_words)

        return medical_words, medical_words_records


class InferenceEngine1(Thread):
    """
    the inference engine that is responsible for decision making.
    """

    def __init__(self, queue: Queue = None, *args, **kwargs):
        super(InferenceEngine1, self).__init__(*args, **kwargs)
        self.queue = queue

    def prepare(self, inference_data: dict) -> None:
        self.text = inference_data.get('text')
        self.patient = inference_data.get('patient')
        self.doctor = inference_data.get('doctor')

    def run(self) -> None:
        from base_backend.messaging import notify_user
        while True:
            inference_data = self.queue.get()
            self.prepare(inference_data=inference_data)
            symptoms, pathologies = self.symptoms_pathologies_graph_maker()
            result = self.inference(symptoms, pathologies)
            # notify the user once the result is ready.
            notify_user(
                self.doctor.profile.user.notification_token.token,
                dict(
                    title="results",
                    alternatives=json.dumps([x.fr for x in result])
                )
            )
            self.queue.task_done()

    def inference(self, symptoms: QuerySet, pathologies: QuerySet) -> list:
        """
        builds the inference engine's decision table from the symptoms-pathology graph.
        :param symptoms:
        :param pathologies:
        :return:
        """
        columns = ["{}".format(symp.name) for symp in symptoms]
        data = []
        for patho in pathologies:
            symtomp = []
            for sym in symptoms:
                symtomp.append(sym in patho.symptoms.all())  # filling each rows with boolean values
            data.append(symtomp)  # appending the row to the decision table

        df_symp_patho = pd.DataFrame(data=data, columns=columns)

        list_patho_score = []
        for index, row in df_symp_patho.iterrows():
            # del row['Pathology']
            list_patho_score.append({'i': index, 'sum': row.sum()})  # true = 1, false = 0
        list_patho_score = sorted(list_patho_score, key=lambda k: k['sum'], reverse=True)
        pathologies_list = [pathologies[item['i']] for item in list_patho_score]
        return pathologies_list  # the ordered list of possible pathologies

    def symptoms_pathologies_graph_maker(self) -> tuple:
        """
        extracts the symptoms found in the text from the database,
        after having the symptoms it brings all the possible pathologies for the set of symptoms
        :return: a tuple containing a set of symptoms and a set of pathologies
        """
        from dictili_medical.models import Symptom, Pathology

        processed_text = pre_processing(self.text)
        query = Q(name__icontains=processed_text[0])
        del processed_text[0]
        for token in processed_text:
            query = query | Q(name__contains=token)
        symptoms = list(Symptom.objects.filter(query).distinct().order_by('id'))[2:]
        pathologies = Pathology.objects.filter(symptoms__in=symptoms).distinct().order_by('id')

        return symptoms, pathologies
