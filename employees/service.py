from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

from models.department import Department
from models.employee import Employee
from models.address import Address
from employees.repository import (
    create_employee,
    delete_employee,
    get_all_employees,
    get_employee_by_id,
    update_employee,
    search_employee_by_name,
    get_employee_addresses,
    add_employee_address,
    update_employee_address,
    remove_employee_address
)

from auth.utils import hash_password

from exceptions import (
    NotFoundException,
    ConflictException
)

async def create(db: AsyncSession, name: str, email: str, phone: str, date_of_birth: str, password: str) -> Employee:
    try:
        employee = await create_employee(
            db=db,
            name=name,
            email=email,
            phone=phone,
            date_of_birth=date.fromisoformat(date_of_birth),
            password=hash_password(password)
        )

        return employee
    except IntegrityError:
        raise ConflictException("Email or phone already exists")

async def get_all(db: AsyncSession) -> list[Employee]:
    return await get_all_employees(db)

async def get_by_id(db: AsyncSession, id: int) -> Employee:
    try:
        return await get_employee_by_id(db, id)
    except NoResultFound:
        raise NotFoundException("Employee does not exist")

async def update(db: AsyncSession, id: int, name: str | None, email: str | None, phone: str | None, date_of_birth: str | None, password: str | None) -> Employee:
    try:
        return await update_employee(
            db=db,
            id=id,
            name=name,
            email=email,
            phone=phone,
            date_of_birth=date.fromisoformat(date_of_birth) if date_of_birth else None,
            password=hash_password(password) if password else None
        )
    except IntegrityError:
        raise ConflictException("Email or phone already exists")
    except NoResultFound:
        raise NotFoundException("Employee does not exist")

async def delete(db: AsyncSession, id: int):
    try:
        await delete_employee(db, id)
    except NoResultFound:
        raise NotFoundException("Employee does not exist")

async def search_by_name(db: AsyncSession, name: str) -> list[Employee]:
    try:
        employees = await search_employee_by_name(db, name)

        return employees
    except NoResultFound:
        return []

async def get_addresses(db: AsyncSession, employee_id: int) -> list[Address]:
    try:
        addresses = await get_employee_addresses(db, employee_id)

        return addresses
    except NoResultFound:
        return []

async def add_address(
    db: AsyncSession,
    employee_id: int,
    line1: str,
    city: str,
    postal_code: str,
    country: str
) -> Address:
    address = await add_employee_address(
        db=db,
        employee_id=employee_id,
        line1=line1,
        city=city,
        postal_code=postal_code,
        country=country
    )
    return address

async def update_address(
    db: AsyncSession,
    address_id: int,
    employee_id: int,
    line1: str | None,
    city: str | None,
    postal_code: str | None,
    country: str | None
) -> Address:
    try:
        address = await update_employee_address(
            db=db,
            address_id=address_id,
            employee_id=employee_id,
            line1=line1,
            city=city,
            postal_code=postal_code,
            country=country
        )

        return address
    except NoResultFound:
        raise NotFoundException("Address entry does not exist for employee")

async def delete_address(
    db: AsyncSession,
    address_id: int,
    employee_id: int
):
    try:
        await remove_employee_address(
            db=db,
            address_id=address_id,
            employee_id=employee_id
        )
    except NoResultFound:
        raise NotFoundException("Address entry does not exist for employee")

async def get_employee_departments(
    db: AsyncSession,
    employee_id: int
) -> list[Department]:
    try:
        return await get_employee_departments(
            db=db,
            employee_id=employee_id
        )
    except NoResultFound:
        raise NotFoundException("Employee not found")
