from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .models import Role
from mcq.models import MCQResult
from subjective.models import SubjectiveAttempt


def home(request):
    roles = Role.objects.all()[:8]
    return render(request, "dashboard/home.html", {"roles": roles})


@login_required
def dashboard(request):
    mcq_results = MCQResult.objects.filter(user=request.user).select_related("role")
    subjective_attempts = SubjectiveAttempt.objects.filter(user=request.user).select_related("role")
    total_interviews = mcq_results.count() + subjective_attempts.count()
    mcq_percentages = [result.percentage for result in mcq_results if result.total_questions]
    subjective_scores = [attempt.score for attempt in subjective_attempts]
    all_scores = mcq_percentages + subjective_scores

    average_score = round(sum(all_scores) / len(all_scores), 1) if all_scores else 0
    best_score = max(all_scores) if all_scores else 0
    accuracy = min(100, round(average_score, 1))

    recent_activity = list(mcq_results.order_by("-date")[:5])
    context = {
        "total_interviews": total_interviews,
        "average_score": average_score,
        "best_score": best_score,
        "accuracy": accuracy,
        "recent_activity": recent_activity,
        "roles": Role.objects.all(),
    }
    return render(request, "dashboard/dashboard.html", context)


@login_required
def role_selection(request):
    return render(request, "dashboard/role_selection.html", {"roles": Role.objects.all()})


@login_required
def interview_type_selection(request, role_id):
    role = get_object_or_404(Role, id=role_id)
    return render(request, "dashboard/interview_type_selection.html", {"role": role})
