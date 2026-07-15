from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class UserType(models.TextChoices):
        ADMIN = "ADMIN", _("مدیر سیستم")
        EXPERT = "EXPERT", _("کارشناس")
        USER = "USER", _("کاربر عادی")

    user_type = models.CharField(
        max_length=200, choices=UserType.choices, default=UserType.USER, verbose_name="نوع کاربر"
    )
    phone_number = models.CharField(max_length=15, null=True, blank=True, unique=True, verbose_name="شماره تلفن")
    national_code = models.CharField(max_length=10, null=True, blank=True, unique=True, verbose_name="کد ملی")
    department = models.CharField(max_length=100, null=True, blank=True, verbose_name="بخش/دپارتمان")
    avatar = models.ImageField(upload_to="avatar/%Y/%m", null=True, blank=True, verbose_name="تصویر پروفایل")
    