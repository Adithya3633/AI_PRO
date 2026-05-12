from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from dashboard.models import Role

from .models import Leaderboard


@login_required
def leaderboard(request):
    role_id = request.GET.get("role")
    entries = Leaderboard.objects.select_related("user", "role")
    if role_id:
        entries = entries.filter(role_id=role_id)
    return render(
        request,
        "leaderboard/leaderboard.html",
        {"entries": entries[:25], "roles": Role.objects.all(), "selected_role": role_id},
    )
