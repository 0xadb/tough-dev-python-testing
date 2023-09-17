from typing import TYPE_CHECKING

import pytest

from http import HTTPStatus
from django.test import Client
from django.urls import reverse


if TYPE_CHECKING:
    from tests.plugins.identity.user import (
            RegistrationData,
            UserAssertion,
            UserData,
            )

@pytest.mark.django_db()
def test_valid_registration(
        client: Client,
        registration_data: "RegistrationData",
        expected_user_data: "UserData",
        assert_correct_user: "UsertAssertion") -> None:
    """Test user registration with correct data."""

    response = client.post(
            reverse("identity:registration"),
            data=registration_data)

    assert response.status_code == HTTPStatus.FOUND
    assert response.get("Location") == reverse("identity:login")
    assert_correct_user(registration_data["email"], expected_user_data)
