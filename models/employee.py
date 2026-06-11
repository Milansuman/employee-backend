from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm.base import Mapped
from sqlalchemy import Text, Date, Enum
from models.entity import Entity
from models.address import Address

import enum

if TYPE_CHECKING:
    from models.department import Department, employee_department
else:
    Department = "Department"
    employee_department = "employee_department"


class EmployeeRoles(enum.Enum):
    ADMIN = "ADMIN"
    HR = "HR"
    ENGINEERING = "ENGINEERING"
    C_SUITE = "C_SUITE"
    UNASSIGNED = "UNASSIGNED"


class EmployeeStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    PROBATION = "PROBATION"
    INACTVE = "INACTIVE"


class Employee(Entity):
    __abstract__ = False
    __tablename__ = "employee"

    name: Mapped[str] = mapped_column(Text, nullable=False)
    phone: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=True)
    joining_date: Mapped[date] = mapped_column(Date, nullable=True)
    experience: Mapped[str] = mapped_column(Text, nullable=True)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    role: Mapped[EmployeeRoles] = mapped_column(
        Enum(EmployeeRoles),
        nullable=False,
        server_default=EmployeeRoles.UNASSIGNED.value,
    )
    status: Mapped[EmployeeStatus] = mapped_column(
        Enum(EmployeeStatus), nullable=False, server_default=EmployeeStatus.ACTIVE.value
    )
    addresses: Mapped[list["Address"]] = relationship(
        Address, back_populates="employee"
    )
    departments: Mapped[list["Department"]] = relationship(
        Department, back_populates="employees", secondary=employee_department
    )

    def to_api_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "date_of_birth": self.date_of_birth.isoformat(),
        }
