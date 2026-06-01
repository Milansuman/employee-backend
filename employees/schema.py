import re
from typing import Annotated

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, PlainSerializer
from datetime import date
from models.employee import EmployeeRoles


def validate_date_format(date_string: str) -> str:
    try:
        date.fromisoformat(date_string)
        return date_string
    except ValueError:
        raise ValueError("Ensure date string is in ISO format (YYYY-MM-DD)")


def validate_phone_number(phone: str) -> str:
    matches = re.match(r"^(\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$", phone)

    if matches is None:
        raise ValueError("Ensure phone number is in the right format")

    return phone


def validate_postal_code(postal_code: str) -> str:
    matches = re.match(r"^\d{3}\s?\d{3}$", postal_code)

    if matches is None:
        raise ValueError("Ensure postal code is accurate")

    return postal_code


def validate_role(role: str) -> str:
    if role not in EmployeeRoles:
        raise ValueError("Invalid role string")

    return role


def date_serializer(date_field: date) -> str:
    return date_field.isoformat()


dobString = Annotated[str, BeforeValidator(validate_date_format)]
phoneString = Annotated[str, BeforeValidator(validate_phone_number)]
postalString = Annotated[str, BeforeValidator(validate_postal_code)]
roleString = Annotated[str, BeforeValidator(validate_role)]
serializedDateString = Annotated[
    date, PlainSerializer(date_serializer, return_type=str)
]


class CreateEmployee(BaseModel):
    name: str = Field(min_length=1)
    email: str = Field(
        min_length=1
    )  # Email cannot be validated with regex. Must use OTP or magic link system. see https://www.regular-expressions.info/email.html
    phone: phoneString = Field(min_length=1)
    dob: dobString = Field(min_length=1)
    password: str = Field(min_length=5)
    role: roleString


class UpdateEmployee(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: phoneString | None = None
    dob: dobString | None = None
    password: str | None = None
    role: roleString | None = None


class CreateEmployeeAddress(BaseModel):
    line1: str = Field(min_length=1)
    city: str = Field(min_length=1)
    postal_code: postalString = Field(min_length=6)
    country: str = Field(min_length=1)


class UpdateEmployeeAddress(BaseModel):
    line1: str | None = None
    city: str | None = None
    postal_code: postalString | None = None
    country: str | None = None


class EmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    phone: str
    date_of_birth: serializedDateString


class EmployeeAddressResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    line1: str
    city: str
    postal_code: str
    country: str
