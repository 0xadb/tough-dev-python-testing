from typing import TYPE_CHECKING, Unpack

import pytest
import random

from mimesis.locales import Locale
from mimesis.schema import Field, Schema

from server.apps.identity.models import User

if TYPE_CHECKING:
    from tests.plugins.identity.user import (
            RegistrationDataFactory,
            RegistrationData,
            UserAssertion,
            UserData,
            )


@pytest.fixture(scope="session")
def assert_correct_user() -> "UserAssertion":
    def factory(email: str, expected: "UserData") -> None:
        user = User.objects.get(email=email)

        assert user.id
        assert user.is_active
        assert not user.is_superuser
        assert not user.is_staff

        for field_name, data_value in expected.items():
            assert getattr(user, field_name) == data_value

    return factory


@pytest.fixture()
def expected_user_data(registration_data: "RegistrationData") -> "UserData":
    """
    We need to simplify registration data to drop passwords.
    Basically, it is the same as ``registration_data``, but without passwords.
    """
    return { # type: ignore[return-value]
            key_name: value_part \
                    for key_name, value_part in registration_data.items() \
                    if not key_name.startswith("password")
            }


@pytest.fixture()
def registration_data_factory() -> "RegistrationDataFactory":
    """Returns factory for fake random data for registration."""

    def factory(**fields: Unpack["RegistrationData"]) -> "RegistrationData":
        mf = Field(locale=Locale.RU)
        password = mf("password")
        schema = Schema(schema=lambda: {
            "email": mf("person.email"),
            "first_name": mf("person.first_name"),
            "last_name": mf("person.last_name"),
            "date_of_birth": mf("datetime.date"),
            "address": mf("address.city"),
            "job_title": mf("person.occupation"),
            "phone": mf("person.telephone"),
            }, iterations=1)
        return {
                **schema.create()[0],
                **{"password1": password, "password2": password},
                **fields
                }

    return factory


@pytest.fixture()
def registration_data(
        registration_data_factory: "RegistrationDataFactory"
        ) -> "RegistrationData":
    """Returns fake random data for registration."""
    return registration_data_factory()
