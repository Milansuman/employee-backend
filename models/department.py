from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Text, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base
from models.entity import Entity, datetime_to_iso

if TYPE_CHECKING:
    from models.employee import Employee
else:
    Employee = "Employee"

employee_department = Table(
    "employee_department",
    Base.metadata,
    Column("employee_id", ForeignKey("employee.id"), primary_key=True),
    Column("department_id", ForeignKey("department.id"), primary_key=True),
)


class Department(Entity):
    __abstract__ = False
    __tablename__ = "department"

    name: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    employees: Mapped[list["Employee"]] = relationship(
        Employee, back_populates="departments", secondary=employee_department
    )

    def to_api_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "created_at": datetime_to_iso(self.created_at),
            "updated_at": datetime_to_iso(self.updated_at),
            "deleted_at": datetime_to_iso(self.deleted_at),
        }
