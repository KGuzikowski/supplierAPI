from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models

from supplierapi.utils.regex import letters_only


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        # Here we just don't return what self.model returns
        # because djongo first need to make few adjustments for MongoDB
        ready_user = self.get(email=email)
        return ready_user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


def user_directory_path(instance: AbstractUser, filename: str) -> str:
    return f"users/{instance.id}/{filename}"


class User(AbstractUser):
    """Default user for supplierAPI."""

    username = None

    first_name = models.CharField(
        max_length=100, validators=[RegexValidator(letters_only)]
    )
    last_name = models.CharField(
        max_length=100, validators=[RegexValidator(letters_only)]
    )
    email = models.EmailField(unique=True)
    profile_image = models.ImageField(
        upload_to=user_directory_path, null=True, blank=True
    )
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=False, null=False, blank=False)
    confirmed = models.BooleanField(null=False, blank=False, default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()
