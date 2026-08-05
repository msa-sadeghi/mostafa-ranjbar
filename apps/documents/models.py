from django.db import models
from django.conf import settings
import uuid
import os
from django.utils import timezone


def document_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1]

    new_filename = f"{uuid.uuid4()}{ext}"
    return os.path.join("documents", str(instance.created_at.year), str(instance.created_at.month), new_filename)


class Folder(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام پوشه")
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children", verbose_name="پوشه مادر"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_folder",
        verbose_name="ایجاد شده توسط",
    )

    level = models.PositiveSmallIntegerField(default=0, verbose_name="سطح", help_text="حداکثر عمق = 10")
    color = models.CharField(max_length=7, default="#4A90D9", verbose_name="رنگ", help_text="کد هگز رنگ")
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.get_full_path()

    def get_full_path(self):
        if self.parent:
            return f"{self.parent.get_full_path()/{self.name}}"
        return self.name

    def get_ancestors(self):
        ancestors = []
        current = self.parent
        while current:
            ancestors.insert(0, current)
            current = current.parent
        return ancestors

    def save(self):
        if self.parent:
            self.level = self.parent.level + 1
            if self.level > 10:
                raise ValueError("max is 10 level")
        else:
            self.level = 0
        super().save()

    class Meta:
        verbose_name = "پوشه"
        verbose_name_plural = "پوشه ها"
        ordering = ["name"]
        unique_together = ["name", "parent"]


class Document(models.Model):
    class StatusChoices(models.TextChoices):
        ACTIVE = "ACTIVE", "فعال"
        ARCHIVED = "ARCHIVED", "بایگانی"
        EXPIRED = "EXPIRED", "منقضی"
        DRAFT = "DRAFT", "پیش نویس"

    class AccessLevel(models.TextChoices):
        PUBLIC = "PUBLIC", "عمومی"
        INTERNAL = "INTERNAL", "داخلی"
        CONFIDENTIAL = "CONFIDENTIAL", "محرمانه"
        SECRET = "SECRET", "سری"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False, verbose_name="شناسه یکتا")
    title = models.CharField(max_length=500, db_index=True, verbose_name="عنوان سند")
    document_number = models.CharField(
        max_length=50, unique=True, verbose_name="شماره سند", help_text="شماره یکتا برای شناسایی سند"
    )
    description = models.TextField(null=True, blank=True, verbose_name="توضیحات")
    file = models.FileField(upload_to=document_upload_path, null=True, blank=True, verbose_name="فایل")
    file_size = models.PositiveIntegerField(null=True, blank=True, verbose_name="حجم فایل بر اساس بایت")
    file_type = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="نوع فایل", help_text="مثل : pdf, xlsx, docx, jpg"
    )

    folder = models.ForeignKey(
        Folder, on_delete=models.SET_NULL, null=True, blank=True, related_name="documents", verbose_name="پوشه"
    )

    tags = models.ManyToManyField("Tag", blank=True, related_name="documents", verbose_name="برچسب ها")

    status = models.CharField(
        max_length=20, choices=StatusChoices.choices, default=StatusChoices.ACTIVE, verbose_name="وضعیت"
    )
    access_level = models.CharField(
        max_length=20, choices=AccessLevel.choices, default=AccessLevel.INTERNAL, verbose_name="سطح دسترسی"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ به روز رسانی")
    expire_date = models.DateField(
        null=True, blank=True, verbose_name="تاریخ  انقضا", help_text="بعد از این تاریخ سند منقضی می شود"
    )

    document_date = models.DateField(null=True, blank=True, verbose_name="تاریخ سند", help_text="تاریخ رسمی سند")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_documents",
        verbose_name="ایجاد  شده  توسط",
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="assigned_documents",
        verbose_name="مسئول پیگیری",
    )
    extra_data = models.JSONField(
        default=dict, blank=True, verbose_name="داده های اضافی", help_text="فیلدهای فرم پویا اینجا ذخیره می شوند"
    )

    def __str__(self):
        return f"[{self.document_number}] {self.title}"

    @property
    def is_expired(self):
        if self.expire_date:
            return self.expire_date < timezone.now().date()
        return False

    @property
    def file_size_human(self):
        if not self.file_size:
            return " نامشخص"
        size = self.file_size
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024:
                return f"{size:.1f}{unit}"
            size /= 1024
        return f"{size:.1f} TB"

    def save(self):
        if self.is_expired and self.status == self.StatusChoices.ACTIVE:
            self.status = self.StatusChoices.EXPIRED
        super().save()
    class Meta:
        verbose = 'سند'
        verbose_name_plural = 'اسناد'
        ordering = ['-created_at']

        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['document_number']),
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['expire_date']),
        ]