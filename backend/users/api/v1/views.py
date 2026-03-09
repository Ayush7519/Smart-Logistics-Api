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
from users.api.v1.blacklist_token_helper import blacklist_all_refresh_tokens
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from django.core.mail import send_mail
from common.middleware import logging_helper
from django.db import transaction
from common.constant.constant import AuditActions
from rest_framework_simplejwt.views import TokenObtainPairView


# -----------------------------------------------------------------------------------------------
# this is the user registration view.(DONE)
# -----------------------------------------------------------------------------------------------
class UserRegisterView(APIView):

    def post(self, request):
        try:
            serializer = serializers.UserRegistration_Serializer(
                data=request.data,
                context={"request": request},
            )

            # here we integrate the logging part for the security purpose.
            if not serializer.is_valid():
                logging_helper.log_warning(
                    request=request,
                    action=AuditActions.USER_REG_FAILED,
                    message="User provided invalid registration data",
                    extra_data={
                        "email": request.data.get("email"),
                        "error_fields": list(serializer.errors.keys()),
                    },
                )
                raise BaseAPIException(
                    message="User provided invalid registration data",
                    code=AuditActions.USER_REG_FAILED,
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            # here we integrate the success log.
            with transaction.atomic():
                user = serializer.save()
            logging_helper.log_success(
                request=request,
                action=AuditActions.USER_REG_SUCCESS,
                message=f"User {user.email} registered successfully",
                user=user,
            )
            return api_response.success_response(
                data="User registered successfully",
                request=request,
            )
        except BaseAPIException:
            raise

        except Exception as e:
            logging_helper.log_error(
                request=request,
                action=AuditActions.USER_REG_ERROR,
                message="An unexpected error occurred during registration",
                error=e,
                extra_data={
                    "email": request.data.get("email"),
                },
            )
            raise BaseAPIException(
                message="An unexpected error occurred during registration",
                code=AuditActions.USER_REG_ERROR,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# -----------------------------------------------------------------------------------------------
# this is the login view.(DONE)
# -----------------------------------------------------------------------------------------------
class UserLoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)

            if response.status_code == 200:
                user_email = request.data.get("email")

                logging_helper.log_success(
                    request=request,
                    action=AuditActions.USER_LOGIN_SUCCESS,
                    message="User logged in successfully.",
                    extra_data={"email": user_email},
                )
                return response

        except Exception as e:
            # Login failed (invalid credentials)
            logging_helper.log_warning(
                request=request,
                action=AuditActions.USER_LOGIN_FAILED,
                message="Invalid login attempt.",
                extra_data={
                    "email": request.data.get("email"),
                },
            )

            raise BaseAPIException(
                message="Invalid credentials.",
                code=AuditActions.USER_LOGIN_FAILED,
                status_code=status.HTTP_401_UNAUTHORIZED,
            )


# -----------------------------------------------------------------------------------------------
# this is the admin creating views.(DONE)
# -----------------------------------------------------------------------------------------------
class AdminCreateUserView(generics.CreateAPIView):
    serializer_class = serializers.AdminCreateUserSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsAdmin,
    ]


# -----------------------------------------------------------------------------------------------
# this is the user profile view.(DONE)
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
# this is the logout view.(DONE)
# -----------------------------------------------------------------------------------------------
class UserLogOutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            # we need the refresh token first.
            refresh_token = request.data.get("refresh")

            # here logging the action.
            if not refresh_token:
                logging_helper.log_warning(
                    request=request,
                    action=AuditActions.USER_LOGOUT_FAILED,
                    message="Refresh token is required.",
                    user=request.user,
                )
                raise BaseAPIException(
                    message="Refresh token is required.",
                    code=AuditActions.USER_LOGOUT_FAILED,
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            with transaction.atomic():
                token = tokens.RefreshToken(refresh_token)
                token.blacklist()

            # here we integrate the success log.
            logging_helper.log_success(
                request=request,
                action=AuditActions.USER_LOGOUT_SUCCESS,
                message="Logged out successfully.",
                user=request.user,
            )
            return api_response.success_response(
                data="Logged out successfully.",
                request=request,
            )

        except TokenError:
            logging_helper.log_warning(
                request=request,
                action=AuditActions.USER_LOGOUT_FAILED,
                message="Invalid or expired refresh token.",
                user=request.user,
            )
            raise BaseAPIException(
                message="Invalid or expired refresh token.",
                code=AuditActions.USER_LOGOUT_FAILED,
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        except BaseAPIException:
            raise

        except Exception as e:
            logging_helper.log_error(
                request=request,
                action=AuditActions.USER_LOGOUT_ERROR,
                message="Unexpected error during logout.",
                error=e,
                user=request.user,
            )
            raise BaseAPIException(
                message="An unexpected error occurred during logout.",
                code=AuditActions.USER_LOGOUT_ERROR,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# -----------------------------------------------------------------------------------------------
# this is the user password change view.(DONE)
# -----------------------------------------------------------------------------------------------
class UserPasswordChangeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            serializer = serializers.UserPasswordChangeSerializer(
                data=request.data,
                context={"request": request},
            )

            # here we add the validation error for the password change.
            if not serializer.is_valid():
                logging_helper.log_warning(
                    request=request,
                    action=AuditActions.PASSWORD_CHANGE_FAILED,
                    message="Invalid password change request.",
                    extra_data={
                        "email": request.user.email,
                        "error_fields": list(serializer.errors.keys()),
                    },
                )
                raise BaseAPIException(
                    message="Invalid password change request.",
                    code=AuditActions.PASSWORD_CHANGE_FAILED,
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            # if the process is success then.
            with transaction.atomic():
                user = request.user
                user.set_password(serializer.validated_data["new_password"])
                user.save()
                # here we block all the login user token after they change the password.
                blacklist_all_refresh_tokens(user)
            logging_helper.log_success(
                request=request,
                action=AuditActions.PASSWORD_CHANGE_SUCCESS,
                message=f"User {user.email} your password has been changed",
                user=user,
            )
            return api_response.success_response(
                data="Password changed successfully.",
                request=request,
            )

        except BaseAPIException:
            raise

        except Exception as e:
            logging_helper.log_error(
                request=request,
                action=AuditActions.PASSWORD_CHANGE_ERROR,
                message="An unexpected error occurred during password change",
                error=e,
            )
            raise BaseAPIException(
                message="An unexpected error occurred during password change",
                code=AuditActions.PASSWORD_CHANGE_ERROR,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# -----------------------------------------------------------------------------------------------
# this is the user forget password view.(DONE)
# -----------------------------------------------------------------------------------------------
class PasswordResetRequestView(APIView):

    def post(self, request):
        try:
            serializer = serializers.PasswordResetRequestSerializer(
                data=request.data,
            )
            if not serializer.is_valid(raise_exception=True):
                logging_helper.log_warning(
                    request=request,
                    action=AuditActions.PASSWORD_RESET_INVALID_REQUEST,
                    message="Invalid password reset request data",
                    extra_data={
                        "error_field": {
                            list(
                                serializer.errors.keys(),
                            )
                        },
                    },
                )
                raise BaseAPIException(
                    message="Invalid request data",
                    code=AuditActions.PASSWORD_RESET_INVALID_REQUEST,
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            # here we take out the email from the frontend.
            email = serializer.validated_data["email"]
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
                logging_helper.log_success(
                    request=request,
                    action=AuditActions.PASSWORD_RESET_REQUEST_SUCCESS,
                    message=f"Password reset link generated for {email}",
                    user=user,
                )
            else:
                logging_helper.log_warning(
                    request=request,
                    action=AuditActions.PASSWORD_RESET_UNKNOWN_EMAIL,
                    message="Password reset requested for non-existent email",
                    extra_data={"email": email},
                )
            return api_response.success_response(
                data="If the email exists, a reset link has been sent.",
                request=request,
            )
        except BaseAPIException:
            raise

        except Exception as e:
            logging_helper.log_error(
                request=request,
                action=AuditActions.PASSWORD_RESET_REQUEST_ERROR,
                message="Unexpected error during password reset request",
                error=e,
                extra_data={"email": request.data.get("email")},
            )

            raise BaseAPIException(
                message="An unexpected error occurred",
                code=AuditActions.PASSWORD_RESET_REQUEST_ERROR,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# -----------------------------------------------------------------------------------------------
# this is the user password changing view through the emial.(DONE)
# -----------------------------------------------------------------------------------------------
class PasswordResetConfirmView(APIView):
    def post(self, request, uid, token):
        try:
            serializer = serializers.PasswordResetConfirmSerializer(
                data=request.data, context={"uid": uid, "token": token}
            )

            if not serializer.is_valid(raise_exception=True):
                logging_helper.log_warning(
                    request=request,
                    action=AuditActions.PASSWORD_RESET_CONFIRM_FAILED,
                    message="Password reset confirmation failed due to invalid token or data",
                    extra_data={
                        "error_fields": list(serializer.errors.keys()),
                        "uid": uid,
                    },
                )
                raise BaseAPIException(
                    message="Invalid or expired reset token.",
                    code=AuditActions.PASSWORD_RESET_CONFIRM_FAILED,
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            user = serializer.validated_data["user"]
            with transaction.atomic():
                user.set_password(serializer.validated_data["new_password"])
                user.save()
                # blocking all the token of the user from the system.
                blacklist_all_refresh_tokens(user)

            logging_helper.log_success(
                request=request,
                action=AuditActions.PASSWORD_RESET_CONFIRM_SUCCESS,
                message=f"Password successfully reset for user {user.email}",
                user=user,
            )
            return api_response.success_response(
                data="Password has been reset successfully.",
                request=request,
            )
        except BaseAPIException:
            raise

        except Exception as e:
            logging_helper.log_error(
                request=request,
                action=AuditActions.PASSWORD_RESET_CONFIRM_ERROR,
                message="Unexpected error during password reset confirmation",
                error=e,
                extra_data={
                    "uid": uid,
                },
            )

            raise BaseAPIException(
                message="An unexpected error occurred",
                code=AuditActions.PASSWORD_RESET_CONFIRM_ERROR,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
