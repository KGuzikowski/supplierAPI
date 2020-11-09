import pytest

from supplierapi.apps.user.models import User
from supplierapi.apps.user.serializers import (
    UserDetailSerializer,
    UserListSerializer,
    UserUpdateSerializer,
)

pytestmark = pytest.mark.django_db


"""Tests for UserDetailSerializer"""


def test_user_detail_serializer_contains_expected_fields(user: User) -> None:
    serializer = UserDetailSerializer(user)
    data = set(serializer.fields.keys())
    expected = {
        "id",
        "email",
        "password",
        "first_name",
        "last_name",
        "profile_image",
        "description",
    }
    assert data == expected


def test_user_detail_serializer_default_data() -> None:
    data = UserDetailSerializer().data
    assert data["email"] == ""
    assert data["first_name"] == ""
    assert data["last_name"] == ""
    assert data["description"] == ""
    assert data["password"] == ""
    assert data["profile_image"] is None


def test_user_detail_serializer_valid() -> None:
    # given only required fields
    input_data = {
        "email": "karol@guz.pl",
        "first_name": "Karol",
        "last_name": "Guzikowski",
        "password": "czesc12",
    }
    serializer = UserDetailSerializer(data=input_data)
    assert serializer.is_valid()
    assert serializer.validated_data == input_data
    input_data.pop("password")
    assert serializer.data == input_data

    # given more than only required fields
    input_data = {
        "email": "karol@guz.pl",
        "first_name": "Karol",
        "last_name": "Guzikowski",
        "password": "czesc12",
        "description": "Hi!",
    }
    serializer = UserDetailSerializer(data=input_data)
    assert serializer.is_valid()
    assert serializer.validated_data == input_data
    input_data.pop("password")
    assert serializer.data == input_data


def test_user_detail_serializer_not_valid_missing_field() -> None:
    input_data = {
        "email": "karol@guz.pl",
        "last_name": "Guzikowski",
        "password": "czesc12",
    }
    serializer = UserDetailSerializer(data=input_data)
    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    input_data.pop("password")
    assert serializer.data == input_data
    assert "first_name" in serializer.errors
    assert serializer.errors["first_name"][0].code == "required"


def test_user_detail_serializer_charfield_invalid() -> None:
    input_data = {
        "email": "karol@guz.pl",
        "last_name": "Guzikowski",
        "first_name": 22,
        "password": "czesc12",
    }
    serializer = UserDetailSerializer(data=input_data)
    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    input_data.pop("password")
    assert serializer.data == input_data
    assert "first_name" in serializer.errors
    assert serializer.errors["first_name"][0].code == "invalid"


def test_user_detail_serializer_email_invalid() -> None:
    input_data = {
        "email": "karolguz.pl",
        "last_name": "Guzikowski",
        "first_name": "Karol",
        "password": "czesc12",
    }
    serializer = UserDetailSerializer(data=input_data)
    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    input_data.pop("password")
    assert serializer.data == input_data
    assert "email" in serializer.errors
    assert serializer.errors["email"][0].code == "invalid"


def test_user_detail_serializer_none_data() -> None:
    serializer = UserDetailSerializer(data=None)
    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    assert serializer.data == {}
    assert "non_field_errors" in serializer.errors
    assert serializer.errors["non_field_errors"][0].code == "null"


"""Tests for UserListSerializer"""


def test_user_list_serializer_contains_expected_fields(user: User) -> None:
    serializer = UserListSerializer(user)
    data = set(serializer.fields.keys())
    expected = {"id", "first_name", "last_name", "profile_image"}
    assert data == expected


def test_user_list_serializer_default_data() -> None:
    data = UserListSerializer().data
    assert data["first_name"] == ""
    assert data["last_name"] == ""
    assert data["profile_image"] is None


def test_user_list_serializer_valid() -> None:
    input_data = {
        "first_name": "Karol",
        "last_name": "Guzikowski",
    }
    serializer = UserListSerializer(data=input_data)
    assert serializer.is_valid()
    assert serializer.validated_data == input_data
    assert serializer.data == input_data


def test_user_list_serializer_not_valid_missing_field() -> None:
    input_data = {
        "last_name": "Guzikowski",
    }
    serializer = UserListSerializer(data=input_data)
    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    assert serializer.data == input_data
    assert "first_name" in serializer.errors
    assert serializer.errors["first_name"][0].code == "required"


def test_user_list_serializer_invalid_field() -> None:
    input_data = {
        "last_name": "Guzikowski",
        "first_name": 22,
    }
    serializer = UserListSerializer(data=input_data)
    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    assert serializer.data == input_data
    assert "first_name" in serializer.errors
    assert serializer.errors["first_name"][0].code == "invalid"


def test_user_list_serializer_none_data() -> None:
    serializer = UserListSerializer(data=None)
    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    assert serializer.data == {}
    assert "non_field_errors" in serializer.errors
    assert serializer.errors["non_field_errors"][0].code == "null"


"""Tests for UserUpdateSerializer"""


def test_user_update_serializer_contains_expected_fields(user: User) -> None:
    serializer = UserUpdateSerializer(user)
    data = set(serializer.fields.keys())
    expected = {
        "id",
        "email",
        "first_name",
        "last_name",
        "profile_image",
        "description",
    }
    assert data == expected


def test_user_update_serializer_default_data() -> None:
    data = UserUpdateSerializer().data
    assert data["first_name"] == ""
    assert data["last_name"] == ""
    assert data["email"] == ""
    assert data["description"] == ""
    assert data["profile_image"] is None


def test_user_update_serializer_valid() -> None:
    input_data = {
        "last_name": "Guzikowski",
    }
    serializer = UserUpdateSerializer(data=input_data)
    assert serializer.is_valid()
    assert serializer.validated_data == input_data
    assert serializer.data == input_data


def test_user_update_serializer_valid_no_field() -> None:
    input_data = {}
    serializer = UserUpdateSerializer(data=input_data)
    assert serializer.is_valid()
    assert serializer.validated_data == {}
    assert serializer.errors == {}
    assert serializer.data == input_data


def test_user_update_serializer_invalid_field() -> None:
    input_data = {
        "first_name": 22,
    }
    serializer = UserUpdateSerializer(data=input_data)
    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    assert serializer.data == input_data
    assert "first_name" in serializer.errors
    assert serializer.errors["first_name"][0].code == "invalid"


def test_user_update_serializer_none_data() -> None:
    serializer = UserUpdateSerializer(data=None)
    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    assert serializer.data == {}
    assert "non_field_errors" in serializer.errors
    assert serializer.errors["non_field_errors"][0].code == "null"
