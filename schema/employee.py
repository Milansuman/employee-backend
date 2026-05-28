from typing import TypedDict

class Employee(TypedDict):
    id: int | None
    name: str | None
    phone: str | None
    email: str | None
    address: str | None
    is_deleted: bool | None

class CreateEmployee(TypedDict):
    name: str
    phone: str
    email: str
    address: str
