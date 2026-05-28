from pydantic import BaseModel

class CreateEmployee(BaseModel):
    name: str
    email: str
    phone: str
    address: str

class UpdateEmployee(BaseModel):
    name: str | None
    email: str | None
    phone: str | None
    address: str | None
