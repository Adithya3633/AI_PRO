from django.contrib import admin

from .models import SubjectiveAttempt


@admin.register(SubjectiveAttempt)
class SubjectiveAttemptAdmin(admin.ModelAdmin):
    list_display = ["user", "role", "score", "created_at"]
    list_filter = ["role", "created_at"]
    search_fields = ["user__username", "question", "feedback"]
