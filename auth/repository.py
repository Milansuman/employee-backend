from sqlalchemy.ext.asyncio import AsyncSession
from models.employee import Employee
from sqlalchemy import select


async def get_employee_by_email(db: AsyncSession, email: str) -> Employee:
    employee = (
        await db.scalars(
            select(Employee)
            .where(Employee.email == email)
            .where(Employee.deleted_at.is_(None))
        )
    ).one()

    return employee
