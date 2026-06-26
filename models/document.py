from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, Integer, ForeignKey
from typing import TYPE_CHECKING

from models.entity import Entity

if TYPE_CHECKING:
    from models.employee import Employee
else:
    Employee = "Employee"


class Document(Entity):
    __tablename__ = "document"
    __abstract__ = False

    filename: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    mime: Mapped[str] = mapped_column(Text, nullable=False)
    employee_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("employee.id"),
        nullable=False,
        index=True,
    )

    employee: Mapped[Employee] = relationship(Employee, back_populates="documents")
