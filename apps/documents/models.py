from django.db import models
from django.conf import settings


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

    