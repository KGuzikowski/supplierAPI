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


class Company(models.Model):
    STATUS_CHOICES = [
        (0, "active"),
        (1, "inactive"),
    ]
    status = models.IntegerField(choices=STATUS_CHOICES)
    name = models.TextField(unique=True)
    name_short = models.CharField(max_length=40)
    description = models.TextField()
    owners = models.ArrayField(model_container=Person)
    staff = models.ArrayField(model_container=Employee)
    roles = models.ArrayField(model_container=Role)
    ceo = models.ArrayField(model_container=Person)
    address = models.EmbeddedField(model_container=Address)
    localizations = models.ArrayField(model_container=Address)

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
    legal_form = models.IntegerField(choices=LEGAL_FORM_CHOICES)
    nip = models.CharField(max_length=10)
    pkd = models.CharField(max_length=11, choices=PKD_OPTIONS)

    created_at = models.DateField(blank=False, null=False, auto_now_add=True)

    objects = models.DjongoManager()

    def __str__(self):
        return self.name
