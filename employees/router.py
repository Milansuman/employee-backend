from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from departments.schema import DepartmentResponse
from employees.schema import CreateEmployee, CreateEmployeeAddress, EmployeeAddressResponse, UpdateEmployee, UpdateEmployeeAddress, EmployeeResponse
from db import get_db
from employees import service as employee_service

from auth.utils import verify_access_token

employee_auth_router = APIRouter(
    prefix="/auth",
    tags=["Employee Authentication"]
)

employee_router = APIRouter(
    prefix="/employee",
    tags=["Employee"],
    dependencies=[Depends(verify_access_token)]
)

@employee_router.get("/all", response_model=list[EmployeeResponse])
async def all_employees(db: AsyncSession = Depends(get_db)):
    employees = await employee_service.get_all(db)
    return employees

@employee_router.post("/", response_model=EmployeeResponse)
async def create_employee(body: CreateEmployee, db: AsyncSession = Depends(get_db)):
    employee = await employee_service.create(
        db=db,
        name=body.name,
        email=body.email,
        phone=body.phone,
        date_of_birth=body.dob,
        password=body.password
    )

    return employee

@employee_router.get("/search", response_model=list[EmployeeResponse])
async def search_employee(name: str, db: AsyncSession = Depends(get_db)):
    employees = await employee_service.search_by_name(db, name)
    return employees

@employee_router.get("/{id}", response_model=EmployeeResponse)
async def get_employee(id: int, db: AsyncSession = Depends(get_db)):
    employee = await employee_service.get_by_id(db, id)
    return employee

@employee_router.patch("/{id}", response_model=EmployeeResponse)
async def update_employee(id: int, body: UpdateEmployee, db: AsyncSession = Depends(get_db)):
    employee = await employee_service.update(
        db=db,
        id=id,
        name=body.name,
        email=body.email,
        phone=body.phone,
        date_of_birth=body.dob,
        password=body.password
    )

    return employee

@employee_router.delete("/{id}")
async def delete_employee(id: int, db: AsyncSession = Depends(get_db)):
    await employee_service.delete(db, id)
    return {
        "detail": "Employee deleted"
    }

@employee_router.get("/{id}/address", response_model=list[EmployeeAddressResponse])
async def get_employee_addresses(id: int, db: AsyncSession = Depends(get_db)):
    employee_addresses = await employee_service.get_addresses(
        db=db,
        employee_id=id
    )

    return employee_addresses

@employee_router.post("/{id}/address", response_model=EmployeeAddressResponse)
async def add_employee_address(id: int, body: CreateEmployeeAddress, db: AsyncSession = Depends(get_db)):
    address = await employee_service.add_employee_address(
        db=db,
        employee_id=id,
        line1=body.line1,
        city=body.city,
        postal_code=body.postal_code,
        country=body.country
    )

    return address

@employee_router.patch("/{employee_id}/address/{address_id}", response_model=EmployeeAddressResponse)
async def update_employee_address(employee_id: int, address_id: int, body: UpdateEmployeeAddress, db: AsyncSession = Depends(get_db)):
    address = await employee_service.update_employee_address(
        db=db,
        employee_id=employee_id,
        address_id=address_id,
        line1=body.line1,
        city=body.city,
        postal_code=body.postal_code,
        country=body.country
    )
    return address

@employee_router.delete("/{employee_id}/address/{address_id}", response_model=EmployeeAddressResponse)
async def delete_employee_address(employee_id: int, address_id: int, db: AsyncSession = Depends(get_db)):
    await employee_service.remove_employee_address(
        db=db,
        employee_id=employee_id,
        address_id=address_id
    )

@employee_router.get("/{employee_id}/department", response_model=list[DepartmentResponse])
async def get_employee_departments(employee_id: int, db: AsyncSession = Depends(get_db)):
    return await employee_service.get_employee_departments(
        db=db,
        employee_id=employee_id
    )
