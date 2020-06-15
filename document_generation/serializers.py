from rest_framework import serializers

from document_generation.models import AudioFile, Word, Document
from document_generation.workers import TranscriptionWorker


class AudioFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioFile
        fields = ['file_location', 'generated_by', 'concerns']

    def create(self, validated_data):
        instance = super(AudioFileSerializer, self).create(validated_data=validated_data)

        return instance


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['word', 'context', 'domain']


class DocumentSerializer(serializers.ModelSerializer):
    audio_file = AudioFileSerializer()

    class Meta:
        model = Document
        fields = ['type', 'words', 'text', 'text_file', 'audio_file']
        extra_kwargs = {
            'words': 'read_only',
            'audio_file': 'read_only',
            'text': 'read_only',
            'type': 'read_only',
            'text_file': 'read_only',
        }
