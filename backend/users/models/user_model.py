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
    def create_user(self, email, password, password2=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", User.Role.ADMIN)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


# -----------------------------------------------------------------------------------------------
# this is the custom user model for the user.
# -----------------------------------------------------------------------------------------------
class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    # here we define the role for the users.
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        MANAGER = "MANAGER", "Manager"
        DRIVER = "DRIVER", "Driver"

    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name="E-mail",
    )
    full_name = models.CharField(
        max_length=50,
        blank=False,
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.MANAGER,
    )
    is_active = models.BooleanField(
        default=True,
    )
    is_staff = models.BooleanField(
        default=True,
    )
    is_verified = models.BooleanField(
        default=False,
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email
