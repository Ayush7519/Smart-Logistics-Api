from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.api.urls")),
    path("api/v1/auth/", include("users.api.v1.urls")),
]
