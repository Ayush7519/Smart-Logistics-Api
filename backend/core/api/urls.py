from django.urls import path
from core.views.health import HelathCheckApi, TestView
from core.api import views

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
    path(
        "audit-logs/",
        views.AuditLogListView.as_view(),
        name="audit-logs",
    ),
]
