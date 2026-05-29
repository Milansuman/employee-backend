from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from employees.repository import get_employee_by_id
from models.department import Department
from models.employee import Employee

async def get_all_departments(
    db: AsyncSession
) -> list[Department]:
    departments = (await db.scalars(
        select(Department)
            .where(Department.deleted_at.is_(None))
    ))

    return list(departments)

async def get_department_by_id(
    db: AsyncSession,
    id: int
) -> Department:
    department = (await db.scalars(
        select(Department)
            .where(Department.id == id)
            .where(Department.deleted_at.is_(None))
    )).one()

    return department

async def search_department_by_name(
    db: AsyncSession,
    name: str
) -> list[Department]:
    departments = (await db.scalars(
        select(Department)
            .where(Department.name.ilike(f"%{name}%"))
            .where(Department.deleted_at.is_(None))
    ))

    return list(departments)

async def create_department(
    db: AsyncSession,
    name: str
) -> Department:
    department = Department(name=name)

    db.add(department)
    await db.commit()

    return department

async def update_department(
    db: AsyncSession,
    id: int,
    name: str
) -> Department:
    department = await get_department_by_id(db, id)

    department.name = name

    db.add(department)
    await db.commit()
    return department

async def delete_department(
    db: AsyncSession,
    id: int
):
    department = await get_department_by_id(db, id)
    department.deleted_at = datetime.now()

    db.add(department)
    await db.commit()

async def add_employee_to_department(
    db: AsyncSession,
    employee_id: int,
    department_id: int
):
    department = await get_department_by_id(db, department_id)
    employee = await get_employee_by_id(db, employee_id)

    department.employees.append(employee)

    db.add(department)
    await db.commit()

async def remove_employee_from_department(
    db: AsyncSession,
    employee_id: int,
    department_id: int
):
    department = await get_department_by_id(db, department_id)
    employee = await get_employee_by_id(db, employee_id)

    department.employees.remove(employee)
    db.add(department)
    await db.commit()

async def get_department_employees(
    db: AsyncSession,
    department_id: int
) -> list[Employee]:
    department = (await db.scalars(
        select(Department)
            .options(selectinload(Department.employees))
            .where(Department.id == department_id)
            .where(Department.deleted_at.is_(None))
    )).one()

    return department.employees
