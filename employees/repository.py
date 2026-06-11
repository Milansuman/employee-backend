from datetime import datetime, date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.address import Address
from models.department import Department
from models.employee import Employee, EmployeeRoles, EmployeeStatus


async def get_all_employees(db: AsyncSession, status: EmployeeStatus | None):
    stmt = select(Employee).where(Employee.deleted_at.is_(None))

    if status:
        stmt = stmt.where(Employee.status == status)

    employees = await db.scalars(stmt)

    return list(employees)


async def get_employee_by_id(db: AsyncSession, id: int):
    employee = (
        await db.scalars(
            select(Employee)
            .where(Employee.id == id)
            .where(Employee.deleted_at.is_(None))
        )
    ).one()

    return employee


async def create_employee(
    db: AsyncSession,
    name: str,
    phone: str,
    email: str,
    date_of_birth: date,
    password: str,
    role: EmployeeRoles,
    experience: str,
    joining_date: date,
    status: EmployeeStatus,
):
    employee = Employee(
        name=name,
        phone=phone,
        email=email,
        date_of_birth=date_of_birth,
        password_hash=password,
        role=role,
        experience=experience,
        joining_date=joining_date,
        status=status,
    )

    db.add(employee)
    await db.commit()

    return employee


async def update_employee(
    db: AsyncSession,
    id: int,
    name: str | None,
    email: str | None,
    phone: str | None,
    date_of_birth: date | None,
    password: str | None,
    role: EmployeeRoles | None,
    experience: str | None,
    joining_date: date | None,
    status: EmployeeStatus | None,
):
    employee = (await db.scalars(select(Employee).where(Employee.id == id))).one()

    employee.name = name if name is not None else employee.name
    employee.email = email if email is not None else employee.email
    employee.phone = phone if phone is not None else employee.phone
    employee.date_of_birth = (
        date_of_birth if date_of_birth is not None else employee.date_of_birth
    )
    employee.password_hash = password if password else employee.password_hash
    employee.role = role if role else employee.role
    employee.experience = experience if experience else employee.experience
    employee.joining_date = joining_date if joining_date else employee.joining_date
    employee.status = status if status else employee.status

    db.add(employee)
    await db.commit()

    return employee


async def delete_employee(db: AsyncSession, id: int):
    employee = (await db.scalars(select(Employee).where(Employee.id == id))).one()
    employee.deleted_at = datetime.now()

    db.add(employee)
    await db.commit()


async def search_employee_by_name(db: AsyncSession, name: str) -> list[Employee]:
    employees = await db.scalars(
        select(Employee)
        .where(Employee.name.ilike(f"%{name}%"))
        .where(Employee.deleted_at.is_(None))
    )
    return list(employees)


async def get_employee_addresses(db: AsyncSession, id: int) -> list[Address]:
    employee = (
        await db.scalars(
            select(Employee)
            .options(selectinload(Employee.addresses))
            .where(Employee.id == id)
            .where(Employee.deleted_at.is_(None))
        )
    ).one()

    return [address for address in employee.addresses if address.deleted_at is None]


async def add_employee_address(
    db: AsyncSession,
    employee_id: int,
    line1: str,
    city: str,
    postal_code: str,
    country: str,
) -> Address:
    address = Address(
        employee_id=employee_id,
        line1=line1,
        city=city,
        postal_code=postal_code,
        country=country,
    )

    db.add(address)
    await db.commit()

    return address


async def update_employee_address(
    db: AsyncSession,
    address_id: int,
    employee_id: int,
    line1: str | None,
    city: str | None,
    postal_code: str | None,
    country: str | None,
) -> Address:
    address = (
        await db.scalars(
            select(Address)
            .where(Address.id == address_id)
            .where(Address.employee_id == employee_id)
            .where(Address.deleted_at.is_(None))
        )
    ).one()

    address.line1 = line1 if line1 is not None else address.line1
    address.city = city if city is not None else address.city
    address.postal_code = (
        postal_code if postal_code is not None else address.postal_code
    )
    address.country = country if country is not None else address.country

    db.add(address)
    await db.commit()

    return address


async def remove_employee_address(db: AsyncSession, address_id: int, employee_id: int):
    address = (
        await db.scalars(
            select(Address)
            .where(Address.id == address_id)
            .where(Address.employee_id == employee_id)
        )
    ).one()

    address.deleted_at = datetime.now()

    db.add(address)
    await db.commit()


async def get_employee_departments(
    db: AsyncSession, employee_id: int
) -> list[Department]:
    employee = (
        await db.scalars(
            select(Employee)
            .options(selectinload(Employee.departments))
            .where(Employee.id == employee_id)
            .where(Employee.deleted_at.is_(None))
        )
    ).one()

    return employee.departments
