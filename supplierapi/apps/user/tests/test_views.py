import pytest
from rest_framework.test import APIClient

from supplierapi.apps.user.models import User

pytestmark = pytest.mark.django_db
client = APIClient()


"""Tests for UserViewSet"""


def test_user_create():
    assert User.objects.count() == 0
    response = client.post(
        "/users/",
        {
            "first_name": "Karol",
            "last_name": "Guzikowski",
            "email": "karol@guz.pl",
            "password": "haslo",
        },
        format="json",
    )
    assert response.status_code == 201
    assert User.objects.count() == 1


def test_user_create_error():
    # first_name wrong
    assert User.objects.count() == 0
    response = client.post(
        "/users/",
        {
            "first_name": 22,
            "last_name": "Guzikowski",
            "email": "karol@guz.pl",
            "password": "haslo",
        },
        format="json",
    )
    assert response.status_code == 400
    assert User.objects.count() == 0

    response = client.post(
        "/users/",
        {
            "first_name": "Kar22ol",
            "last_name": "Guzikowski",
            "email": "karol@guz.pl",
            "password": "haslo",
        },
        format="json",
    )
    assert response.status_code == 400
    assert User.objects.count() == 0

    # last_name wrong
    response = client.post(
        "/users/",
        {
            "first_name": "Karol",
            "last_name": 22,
            "email": "karol@guz.pl",
            "password": "haslo",
        },
        format="json",
    )
    assert response.status_code == 400
    assert User.objects.count() == 0

    response = client.post(
        "/users/",
        {
            "first_name": "Karol",
            "last_name": "Guz22kowski",
            "email": "karol@guz.pl",
            "password": "haslo",
        },
        format="json",
    )
    assert response.status_code == 400
    assert User.objects.count() == 0

    # email wrong
    response = client.post(
        "/users/",
        {
            "first_name": "Karol",
            "last_name": "Guzikowski",
            "email": "karolguz.pl",
            "password": "haslo",
        },
        format="json",
    )
    assert response.status_code == 400
    assert User.objects.count() == 0

    response = client.post(
        "/users/",
        {
            "first_name": "Karol",
            "last_name": "Guzikowski",
            "email": 22,
            "password": "haslo",
        },
        format="json",
    )
    assert response.status_code == 400
    assert User.objects.count() == 0

    # profile image wrong
    response = client.post(
        "/users/",
        {
            "first_name": "Karol",
            "last_name": "Guzikowski",
            "email": "karol@guz.pl",
            "password": "haslo",
            "profile_image": 22,
        },
        format="json",
    )
    assert response.status_code == 400
    assert User.objects.count() == 0


def test_list_users(user: User) -> None:
    assert User.objects.count() == 1
    response = client.get("/users/")
    assert response.status_code == 200
    assert User.objects.count() == 1
    assert len(response.json()) == 1
    assert len(response.json()[0].keys()) == 4
    assert response.json()[0]["id"] == str(user.pk)


def test_get_user(user: User) -> None:
    assert User.objects.count() == 1
    response = client.get(f"/users/{str(user.pk)}/")
    assert response.status_code == 200
    assert User.objects.count() == 1
    assert len(response.json().keys()) == 6
    assert response.json()["id"] == str(user.pk)
    assert response.json()["description"] is None


def test_update_user(user: User) -> None:
    assert User.objects.count() == 1
    description = "Witam!"
    response = client.put(f"/users/{str(user.pk)}/", {"description": description})
    assert response.status_code == 200
    assert User.objects.count() == 1
    assert len(response.json().keys()) == 6
    assert response.json()["id"] == str(user.pk)
    assert response.json()["description"] == description


def test_delete_user(user: User) -> None:
    assert User.objects.count() == 1
    response = client.delete(f"/users/{str(user.pk)}/")
    assert response.status_code == 204
    assert User.objects.count() == 0


"""Test for CustomAuthToken"""


def test_authenticate_wrong_credentials():
    client.post(
        "/users/",
        {
            "first_name": "Karol",
            "last_name": "Guzikowski",
            "email": "karol@guz.pl",
            "password": "haslo",
        },
        format="json",
    )
    response = client.post(
        "/authenticate/", {"username": "karol@guz.pl", "password": "wrong_password"}
    )
    assert response.status_code == 400
    assert "non_field_errors" in response.json()
