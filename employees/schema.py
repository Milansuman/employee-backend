from pydantic import BaseModel

class CreateEmployee(BaseModel):
    name: str
    email: str
    phone: str

class UpdateEmployee(BaseModel):
    name: str | None
    email: str | None
    phone: str | None

class CreateEmployeeAddress(BaseModel):
    line1: str
    city: str
    postal_code: str
    country: str

class UpdateEmployeeAddress(BaseModel):
    line1: str | None
    city: str | None
    postal_code: str | None
    country: str | None
