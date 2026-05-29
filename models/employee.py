from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm.base import Mapped
from sqlalchemy import Text, Date
from models.entity import Entity
from models.address import Address

if TYPE_CHECKING:
    from models.department import Department, employee_department
else:
    Department = "Department"
    employee_department = "employee_department"

class Employee(Entity):
    __abstract__ = False
    __tablename__ = "employee"

    name: Mapped[str] = mapped_column(Text(), nullable=False)
    phone: Mapped[str] = mapped_column(Text(), nullable=False)
    email: Mapped[str] = mapped_column(Text(), nullable=False, unique=True)
    date_of_birth: Mapped[date] = mapped_column(Date(), nullable=True)
    addresses: Mapped[list["Address"]] = relationship(Address, back_populates="employee")
    departments: Mapped[list["Department"]] = relationship(Department, back_populates="employees", secondary=employee_department)

    def to_api_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "date_of_birth": self.date_of_birth.isoformat()
        }
