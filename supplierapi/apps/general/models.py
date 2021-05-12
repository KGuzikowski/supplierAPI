from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models

from supplierapi.utils.regex import letters_spaces_dot, numbers_only


class DialingCode(models.Model):
    code = models.CharField(
        unique=True,
        max_length=3,
        blank=False,
        null=False,
        validators=[RegexValidator(numbers_only), MinLengthValidator(2)],
    )

    class Meta:
        db_table = "DialingCodes"

    def __str__(self):
        return f"+{self.code}"


class PhoneNumber(models.Model):
    number = models.CharField(
        max_length=9,
        blank=False,
        null=False,
        validators=[RegexValidator(numbers_only), MinLengthValidator(9)],
    )
    dialing_code = models.ForeignKey(
        DialingCode, on_delete=models.SET_NULL, null=True, blank=False
    )

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=["dialing_code", "number"],
                name="%(app_label)s_%(class)s_unique_together",
            )
        ]

    def __str__(self):
        return f"+{self.dialing_code} {self.number}"


class Country(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)

    class Meta:
        verbose_name_plural = "Countries"
        db_table = "Countries"

    def __str__(self):
        return self.name


class Address(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False)
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, blank=False, null=True
    )
    city = models.CharField(
        max_length=30,
        blank=False,
        null=False,
        validators=[RegexValidator(letters_spaces_dot)],
    )
    post_code = models.CharField(
        max_length=5,
        blank=False,
        null=False,
        validators=[RegexValidator(numbers_only), MinLengthValidator(5)],
    )
    street = models.CharField(max_length=40, blank=False, null=False)
    house_number = models.CharField(max_length=10, blank=False, null=False)
    local_number = models.CharField(
        max_length=5, blank=True, validators=[RegexValidator(numbers_only)]
    )

    def __str__(self):
        return f"{self.name} - {self.city} {self.street} {self.house_number}"

    class Meta:
        abstract = True
        verbose_name_plural = "Addresses"


class Industry(models.Model):
    name = models.CharField(max_length=60, unique=True, null=False, blank=False)
    parent_industry = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="sub_industries",
        null=True,
        blank=False,
        default=None,
    )

    class Meta:
        verbose_name_plural = "Industries"
        db_table = "Industries"

    def __str__(self):
        return self.name
