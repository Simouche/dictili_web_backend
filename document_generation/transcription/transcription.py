import io

# Imports the Google Cloud client library
import os

from google.cloud import speech_v1
from google.cloud.speech_v1 import enums, types
import io

from dictili.settings import BASE_DIR


class Transcriber:

    def audio_file_reader(self, file_name):
        with io.open(file_name, 'rb') as audio_file:
            content = audio_file.read()
            audio = types.RecognitionAudio(content=content)
        return audio

    def transcribe(self, file_name):
        # Loads the audio into memory
        audio = self.audio_file_reader(file_name)
        config = self.get_config()

        # Instantiates a client
        client = speech.SpeechClient()

        # Detects speech in the audio file
        response = client.recognize(config, audio)

        for result in response.results:
            print('Transcript: {}'.format(result.alternatives[0].transcript))

        return response.results

    def get_config(self):
        config = types.RecognitionConfig(encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
                                         sample_rate_hertz=16000,
                                         language_code='en-US')

        return config


def sample_recognize(local_file_path):
    """
    Transcribe a short audio file using synchronous speech recognition

    Args:
      local_file_path Path to local audio file, e.g. /path/audio.wav
    """

    client = speech_v1.SpeechClient()

    # local_file_path = 'resources/brooklyn_bridge.raw'

    # The language of the supplied audio
    language_code = "fr-FR"

    # Sample rate in Hertz of the audio data sent
    sample_rate_hertz = 8000

    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats.
    encoding = enums.RecognitionConfig.AudioEncoding.AMR
    config = {
        "language_code": language_code,
        "sample_rate_hertz": sample_rate_hertz,
        "encoding": encoding,
    }
    with io.open(local_file_path, "rb") as f:
        content = f.read()
    audio = {"content": content}

    response = client.recognize(config, audio)
    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        print(u"Transcript: {}".format(alternative.transcript))


def execute():
    path = os.path.join(BASE_DIR, 'uploads', 'generated', 'audio', 'Recording.3gp')
    sample_recognize(path)
