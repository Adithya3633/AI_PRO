from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from mcq.models import MCQResult
from subjective.models import SubjectiveAttempt


@login_required
def download_summary_pdf(request):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="interview-report.pdf"'

    pdf = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    y = height - 60

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, y, "AI Interview Preparation Report")
    y -= 35
    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, y, f"Username: {request.user.username}")
    y -= 25

    mcq_results = MCQResult.objects.filter(user=request.user).select_related("role")[:8]
    subjective_attempts = SubjectiveAttempt.objects.filter(user=request.user).select_related("role")[:5]

    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(50, y, "Recent MCQ Scores")
    y -= 20
    pdf.setFont("Helvetica", 10)
    if not mcq_results:
        pdf.drawString(50, y, "No MCQ results yet.")
        y -= 18
    for result in mcq_results:
        pdf.drawString(50, y, f"{result.role.role_name}: {result.score}/{result.total_questions} ({result.percentage}%)")
        y -= 18

    y -= 10
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(50, y, "AI Feedback Highlights")
    y -= 20
    pdf.setFont("Helvetica", 10)
    if not subjective_attempts:
        pdf.drawString(50, y, "No subjective attempts yet.")
        y -= 18
    for attempt in subjective_attempts:
        feedback = attempt.feedback[:90].replace("\n", " ")
        pdf.drawString(50, y, f"{attempt.role.role_name if attempt.role else 'General'}: {attempt.score}/100 - {feedback}")
        y -= 18
        if y < 80:
            pdf.showPage()
            y = height - 60

    pdf.save()
    return response
