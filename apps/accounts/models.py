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

    last_login_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name="آخرین آدرس IP ورود")
    is_verified = models.BooleanField(default=False, verbose_name="تاییدیه دارد؟")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ به روزرسانی")

    @property
    def is_admin(self):
        return self.user_type == self.UserType.ADMIN

    @property
    def is_expert(self):
        return self.user_type == self.UserType.EXPERT

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username

    def __str__(self):
        return f"{self.full_name} ({self.get_user_type_display()})"

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"
        ordering = ["-created_at"]
        db_table = "accounts_user"
