from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.api.v1 import views

urlpatterns = [
    path(
        "register/",
        views.UserRegisterView.as_view(),
        name="register",
    ),
    path(
        "login/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "admin/create-user/",
        views.AdminCreateUserView.as_view(),
        name="admin-create-user",
    ),
    path(
        "me/",
        views.UserProfileView.as_view(),
        name="user profile",
    ),
    path(
        "logout/",
        views.UserLogOutView.as_view(),
        name="logout",
    ),
    path(
        "change-password/",
        views.UserPasswordChangeView.as_view(),
        name="user-password-change",
    ),
    path(
        "password-reset-link/",
        views.PasswordResetRequestView.as_view(),
        name="forget-password-link",
    ),
    path(
        "password-reset-confirm/<uid>/<token>/",
        views.PasswordResetConfirmView.as_view(),
        name="password-reset-link",
    ),
]
