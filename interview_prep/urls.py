from django.contrib import admin
from django.urls import include, path

from dashboard.views import home


urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("accounts/", include("users.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("mcq/", include("mcq.urls")),
    path("subjective/", include("subjective.urls")),
    path("coding/", include("coding.urls")),
    path("leaderboard/", include("leaderboard.urls")),
    path("reports/", include("reports.urls")),
]
