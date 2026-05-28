
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.employee import Employee

async def get_all_employees(db: AsyncSession) -> list[dict]:
    stmt = select(Employee).where(Employee.is_deleted.__eq__(False))
    employees = await db.scalars(stmt)

    return [employee.to_api_dict() for employee in employees]

async def get_employee_by_id(db: AsyncSession, id: int) -> dict:
    employee = (await db.scalars(
        select(Employee)
            .where(Employee.id.__eq__(id))
            .where(Employee.is_deleted.__eq__(False))
    )).one()

    if employee is None:
        raise Exception("Employee not found")

    return employee.to_api_dict()

async def create_employee(db: AsyncSession, employee: dict) -> dict:
    created_employee = Employee(
        name=employee["name"],
        phone=employee["phone"],
        email=employee["email"],
        address=employee["address"],
    )

    db.add(created_employee)
    await db.commit()

    return created_employee.to_api_dict()

async def update_employee(db: AsyncSession, employee: dict):
    employee_to_update = (await db.scalars(
        select(Employee)
            .where(Employee.id.__eq__(employee["id"]))
    )).one()


    employee_to_update.name = employee.get("name", employee_to_update.name)
    employee_to_update.email = employee.get("email", employee_to_update.email)
    employee_to_update.phone = employee.get("phone", employee_to_update.phone)
    employee_to_update.address = employee.get("address", employee_to_update.address)

    db.add(employee_to_update)
    await db.commit()

async def delete_employee(db: AsyncSession, id: int):
    employee_to_delete = (await db.scalars(
        select(Employee)
            .where(Employee.id.__eq__(id))
    )).one()
    employee_to_delete.is_deleted = True

    db.add(employee_to_delete)
    await db.commit()
