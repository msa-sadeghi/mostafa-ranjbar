from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Document, Folder, FormTemplate, DocumentFile, DocumentLog
from .serializers import (
    DocumentFileSerializer,
    DocumentSerializer,
    FolderSerializer,
    FormTemplateSerializer,
    DocumentLogSerializer,
)


class FolderViewSet(viewsets.ModelViewSet):
    queryset = Folder.objects.filter(parent=None)
    serializer_class = FolderSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


class FormTemplateViewSet(viewsets.ModelViewSet):
    queryset = FormTemplate.objects.filter(is_active=True)
    serializer_class = FormTemplateSerializer
