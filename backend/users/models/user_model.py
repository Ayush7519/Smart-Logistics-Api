from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from core.models.base import BaseModel
from common.exceptions.base import BaseAPIException


# -----------------------------------------------------------------------------------------------
# this is the manager of the custome user.
# -----------------------------------------------------------------------------------------------
class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise BaseAPIException(
                message="Email is required",
                code="Email is required",
                status_code=404,
            )

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, password, **extra_fields)


# -----------------------------------------------------------------------------------------------
# this is the custom user model for the user.
# -----------------------------------------------------------------------------------------------
class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name="E-mail",
    )
    full_name = models.CharField(
        max_length=50,
        blank=False,
    )
    is_active = models.BooleanField(
        default=True,
    )
    is_staff = models.BooleanField(
        default=True,
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email
