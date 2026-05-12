from django.urls import path

from . import views


urlpatterns = [
    path("role/<int:role_id>/", views.subjective_interview, name="subjective_interview"),
]
