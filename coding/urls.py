from django.urls import path

from . import views


urlpatterns = [
    path("role/<int:role_id>/", views.coding_challenge, name="coding_challenge"),
]
