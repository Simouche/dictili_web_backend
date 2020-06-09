from rest_framework import serializers

from document_generation.models import AudioFile
from document_generation.workers import TranscriptionWorker


class AudioFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioFile
        fields = ['file_location']

    def create(self, validated_data):
        instance = super(AudioFileSerializer, self).create(validated_data=validated_data)
        transcription_worker = TranscriptionWorker()
        transcription_worker.prepare(instance.file_location.path)
        transcription_worker.start()
        return instance
