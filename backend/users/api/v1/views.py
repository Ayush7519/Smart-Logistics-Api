from users.models.user_model import User
from rest_framework import generics
from rest_framework.views import APIView
from users.api.v1 import serializers
from rest_framework import permissions
from common.responses import api_response
from users.permission import (
    IsAdmin,
    IsManager,
    IsDriver,
)
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework import status
from common.exceptions.base import BaseAPIException
from rest_framework.response import Response
from rest_framework_simplejwt import tokens
from rest_framework_simplejwt.token_blacklist.models import (
    OutstandingToken,
    BlacklistedToken,
)
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from django.core.mail import send_mail


# -----------------------------------------------------------------------------------------------
# this is the user registration view.
# -----------------------------------------------------------------------------------------------
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserRegistration_Serializer


# -----------------------------------------------------------------------------------------------
# this is the admin creating views.
# -----------------------------------------------------------------------------------------------
class AdminCreateUserView(generics.CreateAPIView):
    serializer_class = serializers.AdminCreateUserSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsAdmin,
    ]


# -----------------------------------------------------------------------------------------------
# this is the user profile view.
# -----------------------------------------------------------------------------------------------
class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = serializers.UserProfileSerializer(request.user)
        return api_response.success_response(
            data=serializer.data,
            request=request,
        )


# -----------------------------------------------------------------------------------------------
# this is the logout view.
# -----------------------------------------------------------------------------------------------
class UserLogOutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # we need the refresh token first.
        refresh_token = request.data.get("refresh")
        print("THIS IS THE USER REFRESH TOKEN", refresh_token)
        if not refresh_token:
            raise BaseAPIException(
                message="Refresh token is required.",
                code="REFRESH_TOKEN_REQUIRED",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        try:
            token = tokens.RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            raise BaseAPIException(
                message="Invalid or expired refresh token.",
                code="INVALID_REFRESH_TOKEN",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        return api_response.success_response(
            data="Logged out successfully.",
        )


# -----------------------------------------------------------------------------------------------
# this is the user password change view.
# -----------------------------------------------------------------------------------------------
class UserPasswordChangeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = serializers.UserPasswordChangeSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.set_password(serializer.validated_data["new_password"])
        user.save()

        # here we block all the login user token after they change the password.
        tokens = OutstandingToken.objects.filter(user=user)

        for token in tokens:
            BlacklistedToken.objects.get_or_create(token=token)

        return api_response.success_response(
            data="Password changed successfully.",
        )


# -----------------------------------------------------------------------------------------------
# this is the user forget password view.
# -----------------------------------------------------------------------------------------------
class PasswordResetRequestView(APIView):
    def post(self, request):
        serilaizer = serializers.PasswordResetRequestSerializer(data=request.data)
        serilaizer.is_valid(raise_exception=True)

        # here we take out the email from the frontend.
        email = serilaizer.validated_data["email"]

        # now we takeout the user through the email.
        user = User.objects.filter(email=email).first()

        # now we generate the token if the user is available.
        if user:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            # now we encode the user id.
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # this is the custome reset link.
            reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
            send_mail(
                subject="Password Reset Request",
                message=f"Click the link to reset your password:\n{reset_link}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
            )

        return api_response.success_response(
            data="If the email exists, a reset link has been sent."
        )


# -----------------------------------------------------------------------------------------------
# this is the user password changing view through the emial.
# -----------------------------------------------------------------------------------------------
class PasswordResetConfirmView(APIView):
    def post(self, request, uid, token):
        serializer = serializers.PasswordResetConfirmSerializer(
            data=request.data, context={"uid": uid, "token": token}
        )

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        user.set_password(serializer.validated_data["new_password"])
        user.save()

        # blocking all the token of the user from the system.
        for outstanding in OutstandingToken.objects.filter(user=user):
            BlacklistedToken.objects.get_or_create(token=outstanding)

        return api_response.success_response(
            data="Password has been reset successfully."
        )
