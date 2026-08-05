from django.db import models


class FormSchema(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام فرم")
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="فعال؟")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "قالب فرم"
        verbose_name_plural = " قالب های فرم"


class FormField(models.Model):
    class FieldType(models.TextChoices):
        TEXT = (
            "TEXT",
            "متن",
        )
        NUMBER = (
            "NUMBER",
            "عدد",
        )
        SELECT = (
            "SELECT",
            "انتخاب از لیست",
        )
        DATE = (
            "DATE",
            "تاریخ",
        )
        CHECKBOX = (
            "CHECKBOX",
            "چکباکس",
        )
        FILE = (
            "FILE",
            "فایل",
        )
        TEXTAREA = (
            "TEXTAREA",
            "متن بلند",
        )

    form = models.ForeignKey(FormSchema, on_delete=models.CASCADE, related_name="fields", verbose_name="فرم")
    label = models.CharField(max_length=200, verbose_name='برچسب')
    field_name = models.CharField(max_length=100, verbose_name='نام فیلد (انگلیسی)')
    field_type = models.CharField(
        max_length=20, choices=FieldType.choices,
        default=FieldType.TEXT, verbose_name='نوع فیلد',
    )
    
    is_required = models.BooleanField(default=False, verbose_name='اجباری؟')
    order = models.PositiveSmallIntegerField(default=0, verbose_name='ترتیب')
    
    # برای فیلد SELECT، گزینه‌ها به صورت JSON ذخیره می‌شوند
    options = models.JSONField(
        default=list, blank=True,
        verbose_name='گزینه‌ها',
        help_text='برای نوع SELECT: ["گزینه ۱", "گزینه ۲"]',
    )
    
    placeholder = models.CharField(
        max_length=200, null=True, blank=True,
        verbose_name='متن راهنما',
    )
    
    class Meta:
        verbose_name = 'فیلد فرم'
        verbose_name_plural = 'فیلدهای فرم'
        ordering = ['order']
