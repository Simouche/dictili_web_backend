import os

from django.http import HttpResponse
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from document_generation.models import AudioFile, Document, Word
from document_generation.serializers import AudioFileSerializer, WordSerializer, DocumentSerializer


class AudioFileViewSet(ModelViewSet):
    serializer_class = AudioFileSerializer
    permission_classes = [permissions.AllowAny]
    queryset = AudioFile.objects.all()

    def list(self, request, *args, **kwargs):
        file_path = Document.get_latest()

        file = open(file_path, 'rb')
        file_name = file_path.split("\\")[-1]
        print(file_name)
        response = HttpResponse(file, content_type="application/force-download")
        response['Content-Disposition'] = 'attachment; filename="%s"' % file_name + '.pdf'
        return response


class WordViewSet(ModelViewSet):
    serializer_class = WordSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Word.objects.all()


class DocumentViewSet(ModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Document.objects.All()
