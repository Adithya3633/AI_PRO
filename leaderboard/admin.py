from django.contrib import admin

from .models import Leaderboard


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ["user", "role", "score", "updated_at"]
    list_filter = ["role"]
    search_fields = ["user__username"]
