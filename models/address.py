from sqlalchemy import Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models.entity import Entity

class Address(Entity):
    __abstract__ = False
    __tablename__ = "address"

    line1: Mapped[str] = mapped_column(Text(), nullable=False)
    city: Mapped[str] = mapped_column(Text(), nullable=False)
    postal_code: Mapped[str] = mapped_column(Text(), nullable=False)
    country: Mapped[str] = mapped_column(Text(), nullable=False)
    employee_id: Mapped[int] = mapped_column(
            Integer,
            ForeignKey("employee.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        )
