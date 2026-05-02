from rest_framework import serializers
from .models import Document, Folder, FormTemplate, DocumentFile, DocumentLog


class FolderSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Folder
        fields = "__all__"

    def get_children(self, obj):
        if obj.children.exists():
            return FolderSerializer(obj.children.all(), many=True).data


class DocumentFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentFile
        fields = "__all__"


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"


class FormTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormTemplate
        fields = "__all__"


class DocumentLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentLog
        fields = "__all__"
