import pytest
from bson.objectid import ObjectId

from supplierapi.apps.user.models import User, user_directory_path

pytestmark = pytest.mark.django_db


def test_user_directory_path(user: User) -> None:
    assert user_directory_path(user, "image.jpg") == f"users/{user.pk}/image.jpg"


def test_create_user(user: User) -> None:
    assert isinstance(user.pk, ObjectId)
    assert user.username is None
    assert user.first_name == "Karol"
    assert user.last_name == "Guzikowski"
    assert user.email == "karol@guz.pl"
    assert user.description is None
    assert user.is_active
    assert not user.is_staff
    assert not user.is_superuser


def test_user_update(user: User) -> None:
    user.description = "Jestem Karol i uwielbiam ten serwis!"
    user.save()
    assert user.description == "Jestem Karol i uwielbiam ten serwis!"
