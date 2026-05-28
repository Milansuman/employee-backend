
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.employee import Employee

async def get_all_employees(db: AsyncSession):
    stmt = select(Employee).where(Employee.is_deleted.__eq__(False))
    employees = await db.scalars(stmt)

    return list(employees)

async def get_employee_by_id(db: AsyncSession, id: int):
    employee = (await db.scalars(
        select(Employee)
            .where(Employee.id.__eq__(id))
            .where(Employee.is_deleted.__eq__(False))
    )).one()

    return employee

async def create_employee(db: AsyncSession, name: str, phone: str, email: str, address: str):
    employee = Employee(
        name=name,
        phone=phone,
        email=email,
        address=address,
    )

    db.add(employee)
    await db.commit()

    return employee

async def update_employee(db: AsyncSession, id: int, name: str | None, email: str | None, phone: str | None, address: str | None):
    employee = (await db.scalars(
        select(Employee)
            .where(Employee.id.__eq__(id))
    )).one()


    employee.name = name if name is not None else employee.name
    employee.email = email if email is not None else employee.email
    employee.phone = phone if phone is not None else employee.phone
    employee.address = address if address is not None else employee.address

    db.add(employee)
    await db.commit()

    return employee

async def delete_employee(db: AsyncSession, id: int):
    employee = (await db.scalars(
        select(Employee)
            .where(Employee.id.__eq__(id))
    )).one()
    employee.is_deleted = True

    db.add(employee)
    await db.commit()

async def search_employee_by_name(db: AsyncSession, name: str) -> list[Employee]:
    employees = (await db.scalars(
        select(Employee)
            .where(Employee.name.ilike(f"%{name}%"))
            .where(Employee.is_deleted.__eq__(False))
    ))
    return list(employees)
