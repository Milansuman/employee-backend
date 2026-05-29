from sqlalchemy import Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from models.entity import Entity

if TYPE_CHECKING:
    from models.employee import Employee
else:
    Employee = "Employee"

class Address(Entity):
    __abstract__ = False
    __tablename__ = "address"

    line1: Mapped[str] = mapped_column(Text, nullable=False)
    city: Mapped[str] = mapped_column(Text, nullable=False)
    postal_code: Mapped[str] = mapped_column(Text, nullable=False)
    country: Mapped[str] = mapped_column(Text, nullable=False)
    employee_id: Mapped[int] = mapped_column(
            Integer,
            ForeignKey("employee.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        )
    employee: Mapped["Employee"] = relationship(Employee, back_populates="addresses")

    def to_api_dict(self) -> dict:
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "line1": self.line1,
            "city": self.city,
            "postal_code": self.postal_code,
            "country": self.country
        }
