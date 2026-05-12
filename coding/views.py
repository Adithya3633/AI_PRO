from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from dashboard.models import Role

from .models import CodingAttempt


@login_required
def coding_challenge(request, role_id):
    role = get_object_or_404(Role, id=role_id)
    problem = f"Write a clean solution for a beginner-friendly {role.role_name} coding problem."
    saved = False
    if request.method == "POST":
        submitted_code = request.POST.get("submitted_code", "").strip()
        if submitted_code:
            CodingAttempt.objects.create(
                user=request.user,
                role=role,
                problem_statement=problem,
                submitted_code=submitted_code,
                feedback="Saved for manual or Gemini-based evaluation in Phase 3.",
            )
            saved = True
    return render(
        request,
        "coding/challenge.html",
        {"role": role, "problem": problem, "saved": saved},
    )
