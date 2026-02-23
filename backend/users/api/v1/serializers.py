from rest_framework import serializers
from users.models.user_model import User
from django.contrib.auth.password_validation import validate_password
from common.exceptions.base import BaseAPIException
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


# -----------------------------------------------------------------------------------------------
# this is the user registration views.
# -----------------------------------------------------------------------------------------------
class UserRegistration_Serializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "password2",
            "fullname",
        )

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")
        if password != password2:
            raise serializers.ValidationError(
                {"password": "Passwords do not match."},
            )
        validate_password(password)
        return super().validate(attrs)

    def create(self, validated_data):
        return User.objects.create_user(
            **validated_data,
        )


# -----------------------------------------------------------------------------------------------
# this is the admin creating serializer.
# -----------------------------------------------------------------------------------------------
class AdminCreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "full_name",
            "password",
            "role",
        )

    def validate_role(self, value):
        if value not in [
            User.Role.MANAGER,
            User.Role.DRIVER,
            User.Role.ADMIN,
        ]:
            raise serializers.ValidationError("Invalid role.")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


# -----------------------------------------------------------------------------------------------
# this is the user profile serializer.
# -----------------------------------------------------------------------------------------------
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "role",
            "is_verified",
            "is_active",
            "date_joined",
        )
        read_only_fields = fields


# -----------------------------------------------------------------------------------------------
# this is the user password chage serializer.
# -----------------------------------------------------------------------------------------------
class UserPasswordChangeSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            "old_password",
            "new_password",
            "confirm_password",
        )

    def validate(self, attrs):
        user = self.context["request"].user

        # here checking if the old password match or not.
        if not user.check_password(attrs["old_password"]):
            raise BaseAPIException(
                message="Old password is incorrect.",
                code="INVALID_OLD_PASSWORD",
                status_code=400,
            )

        # here we check if the new password match or not.
        if attrs["new_password"] != attrs["confirm_password"]:
            raise BaseAPIException(
                message="Passwords do not match.",
                code="PASSWORD_MISMATCH",
                status_code=400,
            )

        # using default djagno validation.
        validate_password(attrs["new_password"], user)
        return attrs


# -----------------------------------------------------------------------------------------------
# this is the user forget password serializer.
# -----------------------------------------------------------------------------------------------
class PasswordResetRequestSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ["email"]

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            # Do NOT reveal if email exists (security best practice)
            return value

        return value


# -----------------------------------------------------------------------------------------------
# this is the user password change link serializer.
# -----------------------------------------------------------------------------------------------
class PasswordResetConfirmSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ("new_password", "confirm_password")

    def validate(self, attrs):
        uid = self.context["uid"]
        token = self.context["token"]

        # now we decode the user id.
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except Exception:
            raise BaseAPIException(
                message="Invalid reset link.",
                code="INVALID_LINK",
                status_code=400,
            )
        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            raise BaseAPIException(
                message="Token is invalid or expired.",
                code="INVALID_TOKEN",
                status_code=400,
            )
        if attrs["new_password"] != attrs["confirm_password"]:
            raise BaseAPIException(
                message="Passwords do not match.",
                code="PASSWORD_MISMATCH",
                status_code=400,
            )

        validate_password(attrs["new_password"], user)

        attrs["user"] = user
        return attrs
