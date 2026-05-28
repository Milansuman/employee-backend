from sqlalchemy.orm import mapped_column
from sqlalchemy.orm.base import Mapped
from sqlalchemy import Boolean, Text
from db import Base

class Employee(Base):
    __tablename__ = "employee"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text(), nullable=False)
    phone: Mapped[str] = mapped_column(Text(), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(Text(), nullable=False, unique=True)
    address: Mapped[str] = mapped_column(Text(), nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean(), default=False)

    def to_api_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address
        }
