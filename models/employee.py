from datetime import date

from sqlalchemy.orm import mapped_column
from sqlalchemy.orm.base import Mapped
from sqlalchemy import Text, Date
from models.entity import Entity

class Employee(Entity):
    __abstract__ = False
    __tablename__ = "employee"

    name: Mapped[str] = mapped_column(Text(), nullable=False)
    phone: Mapped[str] = mapped_column(Text(), nullable=False)
    email: Mapped[str] = mapped_column(Text(), nullable=False, unique=True)
    address: Mapped[str] = mapped_column(Text(), nullable=True)
    date_of_birth: Mapped[date] = mapped_column(Date(), nullable=True)

    def to_api_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address
        }
