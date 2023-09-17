from typing import final, TypedDict, TypeAlias, Callable, Protocol, Unpack

import datetime as dt


class UserData(TypedDict, total=False):
    """
    Represent the simplified user data required to create a user.
    It does not include ``password``, because it is very special in django.
    Import this type is only allowed under ``if TYPE_CHECKING`` in tests.
    """
    email: str
    first_name: str
    last_name: str
    date_of_birth: dt.datetime
    address: str
    job_title: str
    phone: str
    phone_type: int


UserAssertion: TypeAlias = Callable[[str, UserData], None]


@final
class RegistrationData(UserData, total=False):
    """
    Represents simplified user data required to create a user.
    Import of this type is only allowed under ``if TYPE_CHECKING`` in tests.
    """
    password1: str
    password2: str


@final
class RegistrationDataFactory(Protocol):
    def __call__(self, **fields: Unpack[RegistrationData]) -> RegistrationData:
        """User data factory protocol"""

