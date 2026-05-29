from fastapi import APIRouter
from fastapi.param_functions import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from employees.schema import CreateEmployee, CreateEmployeeAddress, UpdateEmployee, UpdateEmployeeAddress
from db import get_db
from employees import service as employee_service

employee_router = APIRouter(
    prefix="/employee",
    tags=["Employee"]
)

@employee_router.get("/all")
async def all_employees(db: Annotated[AsyncSession, Depends(get_db)]):
    employees = await employee_service.get_all(db)
    return [employee.to_api_dict() for employee in employees]

@employee_router.post("/")
async def create_employee(body: CreateEmployee, db: Annotated[AsyncSession, Depends(get_db)]):
    employee = await employee_service.create(
        db=db,
        name=body.name,
        email=body.email,
        phone=body.phone,
        date_of_birth=body.dob
    )

    return employee.to_api_dict()

@employee_router.get("/search")
async def search_employee(name: str, db: Annotated[AsyncSession, Depends(get_db)]):
    employees = await employee_service.search_by_name(db, name)
    return [employee.to_api_dict() for employee in employees]

@employee_router.get("/{id}")
async def get_employee(id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    employee = await employee_service.get_by_id(db, id)
    return employee.to_api_dict()

@employee_router.patch("/{id}")
async def update_employee(id: int, body: UpdateEmployee, db: Annotated[AsyncSession, Depends(get_db)]):
    employee = await employee_service.update(
        db=db,
        id=id,
        name=body.name,
        email=body.email,
        phone=body.phone,
        date_of_birth=body.dob
    )

    return employee.to_api_dict()

@employee_router.delete("/{id}")
async def delete_employee(id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    await employee_service.delete(db, id)
    return {
        "detail": "Employee deleted"
    }

@employee_router.get("/{id}/address")
async def get_employee_addresses(id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    employee_addresses = await employee_service.get_addresses(
        db=db,
        employee_id=id
    )

    return [address.to_api_dict() for address in employee_addresses]

@employee_router.post("/{id}/address")
async def add_employee_address(id: int, body: CreateEmployeeAddress, db: Annotated[AsyncSession, Depends(get_db)]):
    address = await employee_service.add_employee_address(
        db=db,
        employee_id=id,
        line1=body.line1,
        city=body.city,
        postal_code=body.postal_code,
        country=body.country
    )

    return address.to_api_dict()

@employee_router.patch("/{employee_id}/address/{address_id}")
async def update_employee_address(employee_id: int, address_id: int, body: UpdateEmployeeAddress, db: Annotated[AsyncSession, Depends(get_db)]):
    address = await employee_service.update_employee_address(
        db=db,
        employee_id=employee_id,
        address_id=address_id,
        line1=body.line1,
        city=body.city,
        postal_code=body.postal_code,
        country=body.country
    )
    return address.to_api_dict()

@employee_router.delete("/{employee_id}/address/{address_id}")
async def delete_employee_address(employee_id: int, address_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    await employee_service.remove_employee_address(
        db=db,
        employee_id=employee_id,
        address_id=address_id
    )
