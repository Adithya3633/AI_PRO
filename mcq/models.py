from django.conf import settings
from django.db import models

from dashboard.models import Role


class MCQQuestion(models.Model):
    DIFFICULTY_CHOICES = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ]

    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="mcq_questions")
    question = models.TextField()
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default="easy")

    class Meta:
        ordering = ["role", "difficulty", "id"]

    def __str__(self):
        return f"{self.role}: {self.question[:60]}"


class MCQResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    total_questions = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    time_taken = models.PositiveIntegerField(help_text="Time taken in seconds")

    class Meta:
        ordering = ["-date"]

    @property
    def percentage(self):
        if not self.total_questions:
            return 0
        return round((self.score / self.total_questions) * 100)

    def __str__(self):
        return f"{self.user} - {self.role} - {self.score}/{self.total_questions}"
