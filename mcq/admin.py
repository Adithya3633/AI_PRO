from django.contrib import admin

from .models import MCQQuestion, MCQResult


@admin.register(MCQQuestion)
class MCQQuestionAdmin(admin.ModelAdmin):
    list_display = ["question", "role", "difficulty", "correct_answer"]
    list_filter = ["role", "difficulty"]
    search_fields = ["question", "option1", "option2", "option3", "option4"]


@admin.register(MCQResult)
class MCQResultAdmin(admin.ModelAdmin):
    list_display = ["user", "role", "score", "total_questions", "time_taken", "date"]
    list_filter = ["role", "date"]
    search_fields = ["user__username"]
