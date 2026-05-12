from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, render

from dashboard.models import Role

from .models import SubjectiveAttempt
from .services import gemini_evaluate_answer, gemini_generate_question


@login_required
def subjective_interview(request, role_id):
    role = get_object_or_404(Role, id=role_id)
    question = request.POST.get("question") or gemini_generate_question(role.role_name)
    result = None
    if request.method == "POST":
        answer = request.POST.get("answer", "").strip()
        if answer:
            result = gemini_evaluate_answer(question, answer)
            SubjectiveAttempt.objects.create(
                user=request.user,
                role=role,
                question=question,
                answer=answer,
                feedback=result["feedback"],
                score=result["score"],
            )
        else:
            messages.error(request, "Please type an answer before submitting.")
    return render(
        request,
        "subjective/interview.html",
        {"role": role, "question": question, "result": result},
    )
