from djongo import models

from .pkd_options import PKD_OPTIONS


class Person(models.Model):
    user_id = models.CharField()

    class Meta:
        abstract = True


class Employee(Person):
    role = models.CharField(max_length=30)

    class Meta:
        abstract = True


class Role(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Address(models.Model):
    COUNTRY_CHOICES = [
        ("pl", "Poland"),
    ]
    country = models.CharField(max_length=3, choices=COUNTRY_CHOICES)
    city = models.CharField(max_length=30)
    post_code = models.CharField(max_length=6)
    street = models.CharField(max_length=40)
    house_number = models.CharField(max_length=10)
    local_number = models.CharField(max_length=5)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.street} {self.city}"


def company_directory_path(instance, filename):
    return f"companies/{instance.pk}/{filename}"


class Company(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    STATUS_CHOICES = [
        (0, "active"),
        (1, "inactive"),
    ]
    status = models.IntegerField(choices=STATUS_CHOICES, null=False, blank=False)
    name = models.TextField(unique=True, null=False, blank=False)
    short_name = models.CharField(max_length=40, default=None)
    description = models.TextField(null=False, blank=False)
    profile_image = models.ImageField(default=None, upload_to=company_directory_path)
    owners = models.ArrayField(model_container=Person, default=[])
    staff = models.ArrayField(model_container=Employee, default=[])
    roles = models.ArrayField(model_container=Role, default=[])
    address = models.EmbeddedField(model_container=Address, null=False, blank=False)
    localizations = models.ArrayField(model_container=Address, default=[])

    LEGAL_FORM_CHOICES = [
        (0, "jednoosobowa działalność gospodarcza"),
        (1, "spółka cywilna"),
        (2, "spółka jawna"),
        (3, "spółka partnerska"),
        (4, "spółka komandytowa"),
        (5, "spółka komandytowo-akcyjna"),
        (6, "spółka z ograniczoną odpowiedzialnością"),
        (7, "spółka akcyjna"),
        (8, "fundacja"),
        (9, "szkoła/uczelnia wyższa"),
        (10, "inne"),
    ]
    legal_form = models.IntegerField(
        choices=LEGAL_FORM_CHOICES, null=False, blank=False
    )
    nip = models.CharField(max_length=10, null=False, blank=False)
    pkd = models.CharField(max_length=11, choices=PKD_OPTIONS, null=False, blank=False)

    created_at = models.DateField(blank=False, null=False, auto_now_add=True)

    objects = models.DjongoManager()

    def __str__(self):
        return self.name
