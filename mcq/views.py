import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

from dashboard.models import Role
from leaderboard.models import Leaderboard

from .models import MCQQuestion, MCQResult


@login_required
def start_test(request, role_id):
    role = get_object_or_404(Role, id=role_id)
    question_count = MCQQuestion.objects.filter(role=role).count()
    return render(request, "mcq/start.html", {"role": role, "question_count": question_count})


@login_required
@ensure_csrf_cookie
def take_test(request, role_id):
    role = get_object_or_404(Role, id=role_id)
    questions = list(MCQQuestion.objects.filter(role=role).order_by("?")[:10])
    payload = [
        {
            "id": question.id,
            "question": question.question,
            "options": [question.option1, question.option2, question.option3, question.option4],
        }
        for question in questions
    ]
    return render(
        request,
        "mcq/test.html",
        {
            "role": role,
            "questions": payload,
            "duration_seconds": max(300, len(questions) * 60),
        },
    )


@login_required
@require_POST
def submit_test(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    role = get_object_or_404(Role, id=data.get("role_id"))
    answers = data.get("answers", {})
    time_taken = int(data.get("time_taken", 0))
    questions = MCQQuestion.objects.filter(id__in=answers.keys(), role=role)
    score = 0
    total = questions.count()

    for question in questions:
        if answers.get(str(question.id)) == question.correct_answer:
            score += 1

    result = MCQResult.objects.create(
        user=request.user,
        role=role,
        score=score,
        total_questions=total,
        time_taken=time_taken,
    )
    leaderboard_entry = Leaderboard.objects.filter(user=request.user, role=role).first()
    best_score = max(score, leaderboard_entry.score if leaderboard_entry else 0)
    Leaderboard.objects.update_or_create(
        user=request.user,
        role=role,
        defaults={"score": best_score},
    )
    return JsonResponse({"redirect_url": f"/mcq/result/{result.id}/"})


@login_required
def result_detail(request, result_id):
    result = get_object_or_404(MCQResult, id=result_id, user=request.user)
    return render(request, "mcq/result.html", {"result": result})
