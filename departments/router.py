from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from departments import service
from departments.schema import CreateOrUpdateDepartment, DepartmentResponse
from employees.schema import EmployeeResponse

from auth.dependencies import verify_access_token, require_roles
from models.employee import EmployeeRoles

department_router = APIRouter(
    prefix="/department",
    tags=["Department"],
    dependencies=[Depends(verify_access_token)],
)

@department_router.get(
    "/all",
    response_model=list[DepartmentResponse],
    dependencies=[Depends(require_roles([EmployeeRoles.HR, EmployeeRoles.ADMIN]))],
)
async def get_all_departments(db: AsyncSession = Depends(get_db)):
    return await service.get_all_departments(db)


@department_router.get(
    "/search",
    response_model=list[DepartmentResponse],
    dependencies=[Depends(require_roles([EmployeeRoles.HR, EmployeeRoles.ADMIN]))],
)
async def search_department(name: str, db: AsyncSession = Depends(get_db)):
    return await service.search_department_by_name(db, name)


@department_router.get(
    "/{id}",
    response_model=DepartmentResponse,
    dependencies=[Depends(require_roles([EmployeeRoles.HR, EmployeeRoles.ADMIN]))],
)
async def get_department(id: int, db: AsyncSession = Depends(get_db)):
    return await service.get_department_by_id(db, id)


@department_router.post(
    "/",
    response_model=DepartmentResponse,
    dependencies=[Depends(require_roles([EmployeeRoles.HR, EmployeeRoles.ADMIN]))],
)
async def create_department(
    body: CreateOrUpdateDepartment, db: AsyncSession = Depends(get_db)
):
    return await service.create_department(db=db, name=body.name)


@department_router.patch(
    "/{id}",
    response_model=DepartmentResponse,
    dependencies=[Depends(require_roles([EmployeeRoles.HR, EmployeeRoles.ADMIN]))],
)
async def update_department(
    id: int, body: CreateOrUpdateDepartment, db: AsyncSession = Depends(get_db)
):
    return await service.update_department(db=db, id=id, name=body.name)


@department_router.delete(
    "/{id}", dependencies=[Depends(require_roles([EmployeeRoles.HR, EmployeeRoles.ADMIN]))]
)
async def delete_department(id: int, db: AsyncSession = Depends(get_db)):
    await service.delete_department(db=db, id=id)


@department_router.get(
    "/{id}/employee",
    response_model=list[EmployeeResponse],
    dependencies=[Depends(require_roles([EmployeeRoles.HR, EmployeeRoles.ADMIN]))],
)
async def get_department_employees(id: int, db: AsyncSession = Depends(get_db)):
    return await service.get_department_employees(db=db, id=id)


@department_router.put(
    "/{id}/employee", dependencies=[Depends(require_roles([EmployeeRoles.HR, EmployeeRoles.ADMIN]))]
)
async def add_employee_to_department(
    id: int, employee_id: int, db: AsyncSession = Depends(get_db)
):
    await service.add_department_employee(
        db=db, employee_id=employee_id, department_id=id
    )


@department_router.delete(
    "/{id}/employee", dependencies=[Depends(require_roles([EmployeeRoles.HR, EmployeeRoles.ADMIN]))]
)
async def remove_employee_from_department(
    id: int, employee_id: int, db: AsyncSession = Depends(get_db)
):
    await service.remove_department_employee(
        db=db, employee_id=employee_id, department_id=id
    )
