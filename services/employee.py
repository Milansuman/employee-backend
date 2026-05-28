from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from models.employee import Employee
from repositories.employee import (
    create_employee,
    delete_employee,
    get_all_employees,
    get_employee_by_id,
    update_employee,
    search_employee_by_name
)

async def create(db: AsyncSession, name: str, email: str, phone: str, address: str) -> Employee:
    try:
        employee = await create_employee(
            db=db,
            name=name,
            email=email,
            phone=phone,
            address=address
        )

        return employee
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Duplicate email or phone number"
        )

async def get_all(db: AsyncSession) -> list[Employee]:
    return await get_all_employees(db)

async def get_by_id(db: AsyncSession, id: int) -> Employee:
    try:
        return await get_employee_by_id(db, id)
    except NoResultFound:
        raise HTTPException(
            status_code=404,
            detail="Employee does not exist"
        )

async def update(db: AsyncSession, id: int, name: str | None, email: str | None, phone: str | None, address: str | None) -> Employee:
    try:
        return await update_employee(
            db=db,
            id=id,
            name=name,
            email=email,
            phone=phone,
            address=address
        )
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Duplicate email or phone number"
        )
    except NoResultFound:
        raise HTTPException(
            status_code=404,
            detail="Employee does not exist"
        )

async def delete(db: AsyncSession, id: int):
    try:
        await delete_employee(db, id)
    except NoResultFound:
        raise HTTPException(
            status_code=404,
            detail="Employee does not exist"
        )

async def search_by_name(db: AsyncSession, name: str) -> list[Employee]:
    try:
        employees = await search_employee_by_name(db, name)

        return employees
    except NoResultFound:
        return []
