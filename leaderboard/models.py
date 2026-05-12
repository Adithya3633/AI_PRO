from django.conf import settings
from django.db import models

from dashboard.models import Role


class Leaderboard(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-score", "updated_at"]
        unique_together = ["user", "role"]

    def __str__(self):
        return f"{self.user} - {self.role} - {self.score}"
