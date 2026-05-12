from django.conf import settings
from django.db import models

from dashboard.models import Role


class CodingAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    problem_statement = models.TextField()
    submitted_code = models.TextField()
    feedback = models.TextField(blank=True)
    score = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.role} coding attempt"
