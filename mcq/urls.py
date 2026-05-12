from django.urls import path

from . import views


urlpatterns = [
    path("role/<int:role_id>/start/", views.start_test, name="mcq_start"),
    path("role/<int:role_id>/test/", views.take_test, name="mcq_test"),
    path("submit/", views.submit_test, name="mcq_submit"),
    path("result/<int:result_id>/", views.result_detail, name="mcq_result"),
]
