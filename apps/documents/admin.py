from django.contrib import admin
from .models import Folder, Document, DocumentVersion, DocumentLog
from django.utils.html import format_html


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ["name", "parent", "level", "created_by", "created_at"]
    list_filter = ["level"]
    search_fields = ["name"]


class DocumentVersionInline(admin.TabularInline):
    model = DocumentVersion


class DocumnetLogInline(admin.StackedInline):
    model = DocumentLog


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = [
        "document_number",
        "title",
        "folder",
        "status_badge",
        "access_level",
        "is_expired",
        "created_by",
        "created_at",
    ]
    list_filter = ["status", "access_level", "file_type", "created_at"]
    search_fields = ["title", "document_number", "description"]
    date_hierarchy = "created_at"
    readonly_fields = ["id", "file_size", "file_type", "created_at", "updated_at"]

    def status_badge(self, obj):
        colors = {
            "ACTIVE": "green",
            "ARCHIVED": "brown",
            "EXPIRED": "red",
            "DRAFT": "blue",
        }
        color = colors.get(obj.status)
        return format_html('<span style="background:{}; border-radius:4px;>{}</span>', color, obj.status)

    status_badge.short_description = "وضعیت"

    inlines = [DocumentVersionInline, DocumnetLogInline]
