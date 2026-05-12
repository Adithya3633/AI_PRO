from django.contrib import admin

from .models import CodingAttempt


@admin.register(CodingAttempt)
class CodingAttemptAdmin(admin.ModelAdmin):
    list_display = ["user", "role", "score", "created_at"]
    list_filter = ["role", "created_at"]
    search_fields = ["user__username", "problem_statement", "submitted_code"]
