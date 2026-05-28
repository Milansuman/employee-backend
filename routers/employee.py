from fastapi import APIRouter
from fastapi.param_functions import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from schema.employee import CreateEmployee, UpdateEmployee
from db import get_db
from services import employee_service

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
        address=body.address
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
        address=body.address
    )

    return employee.to_api_dict()

@employee_router.delete("/{id}")
async def delete_employee(id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    await employee_service.delete(db, id)
    return {
        "detail": "Employee deleted"
    }
