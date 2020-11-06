from django.contrib.auth.models import AbstractUser, BaseUserManager
from djongo import models


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


def user_directory_path(instance, filename):
    return f"users/{instance.pk}/{filename}"


class User(AbstractUser):
    """Default user for supplierAPI."""

    username = None
    id = None

    _id = models.ObjectIdField(primary_key=True)
    first_name = models.CharField(help_text="first name", max_length=150)
    last_name = models.CharField(help_text="last name", max_length=150)
    email = models.EmailField(help_text="email address", unique=True)
    profile_image = models.ImageField(default=None, upload_to=user_directory_path)
    description = models.TextField(default=None)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()
