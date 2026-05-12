from django.urls import path

from . import views


urlpatterns = [
    path("summary.pdf", views.download_summary_pdf, name="download_summary_pdf"),
]
