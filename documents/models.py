from django.db import models
from users.models import User


class Folder(models.Model):

    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="children", null=True, blank=True
    )
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    level = models.IntegerField(default=0)

    class Meta:
        db_table = "folders"

    def save(self, *args, **kwargs):
        if self.parent:
            self.level = self.parent.level + 1
            if self.level > 10:
                raise ValueError("max depth is 10")

        super().save(*args, **kwargs)


class FormTemplate(models.Model):
    name = models.CharField(max_length=255)
    fields = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "form_templates"


class Document(models.Model):
    title = models.CharField(max_length=500)
    folder = models.ForeignKey(
        Folder, on_delete=models.SET_NULL, null=True, related_name="documents"
    )
    parent_document = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="sub_documents",
    )
    form_data = models.JSONField(default=dict)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="created_documents"
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_documents",
    )
    expiry_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "documents"
        ordering = ["-created_at"]


class DocumentFile(models.Model):
    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name="files"
    )
    file = models.FileField(upload_to="documents/%Y/%m/%d/")
    file_type = models.CharField(max_length=50)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "documents_files"


class DocumentLog(models.Model):
    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name="logs"
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    changes = models.JSONField(default=dict)

    class Meta:
        db_table = "document_logs"
        ordering = ["-timestamp"]
