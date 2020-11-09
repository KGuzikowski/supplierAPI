import pytest

from supplierapi.apps.user.models import User


@pytest.fixture
def user() -> User:
    """Returns user"""
    return User.objects.create_user(
        first_name="Karol",
        last_name="Guzikowski",
        email="karol@guz.pl",
    )
