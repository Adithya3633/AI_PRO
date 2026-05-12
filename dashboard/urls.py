from django.urls import path

from . import views


urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("roles/", views.role_selection, name="role_selection"),
    path("roles/<int:role_id>/types/", views.interview_type_selection, name="interview_type_selection"),
]
