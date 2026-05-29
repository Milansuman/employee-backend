from typing import Annotated

from pydantic import BaseModel, BeforeValidator
from datetime import date

def validate_date_format(date_string: str) -> str:
    try:
        date.fromisoformat(date_string)
        return date_string
    except ValueError:
        raise ValueError("Ensure date string is in ISO format (YYYY-MM-DD)")

class CreateEmployee(BaseModel):
    name: str
    email: str
    phone: str
    dob: Annotated[str, BeforeValidator(validate_date_format)]

class UpdateEmployee(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    dob: Annotated[str, validate_date_format] | None = None

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
