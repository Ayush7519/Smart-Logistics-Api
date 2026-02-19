from django.urls import path
from core.views.health import HelathCheckApi, TestView

urlpatterns = [
    path(
        "health/",
        HelathCheckApi.as_view(),
        name="health-check",
    ),
    path(
        "try/",
        TestView.as_view(),
        name="trsting the exception handeling",
    ),
]
