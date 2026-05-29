from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from departments import repository
from models.department import Department

from exceptions import (
    NotFoundException,
    ConflictException
)
from models.employee import Employee

async def get_all_departments(
    db: AsyncSession
) -> list[Department]:
    try:
        return await repository.get_all_departments(db)
    except NoResultFound:
        return []

async def get_department_by_id(
    db: AsyncSession,
    id: int
) -> Department:
    try:
        return await repository.get_department_by_id(db, id)
    except NoResultFound:
        raise NotFoundException("Department does not exist")

async def search_department_by_name(
    db: AsyncSession,
    name: str
) -> list[Department]:
    try:
        return await repository.search_department_by_name(db, name)
    except NoResultFound:
        return []

async def create_department(
    db: AsyncSession,
    name: str
) -> Department:
    try:
        return await repository.create_department(db, name)
    except IntegrityError:
        raise ConflictException("Department already exists")

async def update_department(
    db: AsyncSession,
    id: int,
    name: str
) -> Department:
    try:
        return await repository.update_department(db, id, name)
    except IntegrityError:
        raise ConflictException("Department name already exists")
    except NoResultFound:
        raise NotFoundException("Department does not exist")

async def delete_department(
    db: AsyncSession,
    id: int
):
    try:
        await repository.delete_department(db, id)
    except NoResultFound:
        raise NotFoundException("Department does not exist")

async def get_department_employees(
    db: AsyncSession,
    id: int
) -> list[Employee]:
    try:
        return await repository.get_department_employees(db, id)
    except NoResultFound:
       raise NotFoundException("Department does not exist")

async def add_department_employee(
    db: AsyncSession,
    employee_id: int,
    department_id: int
):
    await repository.add_employee_to_department(db, employee_id, department_id)

async def remove_department_employee(
    db: AsyncSession,
    employee_id: int,
    department_id: int
):
    await repository.remove_employee_from_department(db, employee_id, department_id)
