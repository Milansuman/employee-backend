from typing import Annotated

from pydantic import BaseModel, BeforeValidator, ConfigDict, PlainSerializer
from datetime import date

def validate_date_format(date_string: str) -> str:
    try:
        date.fromisoformat(date_string)
        return date_string
    except ValueError:
        raise ValueError("Ensure date string is in ISO format (YYYY-MM-DD)")

def date_serializer(date_field: date) -> str:
    return date_field.isoformat()

dobString = Annotated[str, BeforeValidator(validate_date_format)]
serializedDateString = Annotated[date, PlainSerializer(date_serializer, return_type=str)]

class CreateEmployee(BaseModel):
    name: str
    email: str
    phone: str
    dob: dobString

class UpdateEmployee(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    dob: dobString | None = None

class CreateEmployeeAddress(BaseModel):
    line1: str
    city: str
    postal_code: str
    country: str

class UpdateEmployeeAddress(BaseModel):
    line1: str | None = None
    city: str | None = None
    postal_code: str | None = None
    country: str | None = None

class EmployeeResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    name: str
    email: str
    phone: str
    date_of_birth: serializedDateString

class EmployeeAddressResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    line1: str
    city: str
    postal_code: str
    country: str
