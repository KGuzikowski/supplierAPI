from django.conf import settings
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models

from supplierapi.apps.general import models as general_models
from supplierapi.utils.regex import letters_spaces_dot, number_VAT


def company_directory_path(instance: models.Model, filename: str) -> str:
    return f"companies/{instance.id}/{filename}"


class Company(models.Model):
    STATUS_CHOICES = [
        (0, "active"),
        (1, "inactive"),
    ]
    status = models.IntegerField(
        choices=STATUS_CHOICES, null=False, blank=False, default=1
    )
    country_of_registration = models.ForeignKey(
        general_models.Country, on_delete=models.SET_NULL, blank=False, null=True
    )
    name = models.CharField(unique=True, null=False, blank=False, max_length=200)
    short_name = models.CharField(max_length=40, default=None, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(
        upload_to=company_directory_path, null=True, blank=True
    )
    owners = models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=False)

    number_VAT = models.CharField(
        unique=True,
        max_length=12,
        null=False,
        blank=False,
        validators=[RegexValidator(number_VAT), MinLengthValidator(10)],
    )
    industry = models.ForeignKey(
        general_models.Industry, on_delete=models.SET_NULL, blank=False, null=True
    )
    confirmed = models.BooleanField(null=False, blank=False, default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Companies"


class Address(general_models.Address):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="localizations",
        null=False,
        blank=False,
    )


class Role(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="roles", null=False, blank=False
    )
    name = models.CharField(
        max_length=30,
        blank=False,
        null=False,
        validators=[RegexValidator(letters_spaces_dot)],
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["company", "name"],
                name="%(app_label)s_%(class)s_unique_together",
            )
        ]

    def __str__(self):
        return self.name


class Employee(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="staff", null=False, blank=False
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, blank=False, null=False, on_delete=models.CASCADE
    )
    roles = models.ManyToManyField(to=Role, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["company", "user"],
                name="%(app_label)s_%(class)s_unique_together",
            )
        ]

    def __str__(self):
        return f"{self.company.name} - {self.user.first_name} {self.user.last_name}"


class PhoneNumber(general_models.PhoneNumber):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="phone_numbers",
        null=False,
        blank=False,
    )
