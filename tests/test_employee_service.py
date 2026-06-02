import pytest
from datetime import date
from employees import service as employee_service
from models.employee import Employee, EmployeeRoles


@pytest.mark.asyncio
async def test_create_employee_persists_the_record(db_session):
    employee = await employee_service.create(
        db=db_session,
        name="Ada",
        email="ada@example.com",
        password="secret123",
        phone="1234567890",
        date_of_birth="2000-01-01",
        role="UNASSIGNED",
    )

    assert employee.id is not None
    assert employee.name == "Ada"
    assert employee.email == "ada@example.com"


@pytest.mark.asyncio
async def test_employee_get_by_id(db_session):
    seeded_employee = Employee(
        name="Ada",
        email="ada@example.com",
        password_hash="secret123",
        phone="1234567890",
        date_of_birth=date.today(),
        role=EmployeeRoles.UNASSIGNED,
    )

    db_session.add(seeded_employee)
    await db_session.commit()

    employee = await employee_service.get_by_id(db=db_session, id=seeded_employee.id)

    assert seeded_employee == employee
