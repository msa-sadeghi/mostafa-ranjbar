from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [
        ("admin", "مدیر"),
        ("expert", "کارشناس"),
        ("user", "کاربر"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user")
    phone = models.CharField(max_length=15, blank=True)

    class Meta:
        db_table = "users"
class UserLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="logs")
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True)
    details = models.JSONField(default=dict)

    class Meta:
        db_table = "user_logs"
        ordering = ["-timestamp"]
