import pytest
from departments import service as department_service
from exceptions import NotFoundException


@pytest.mark.asyncio
async def test_create_department_persists_record(db_session):
    department = await department_service.create_department(
        db=db_session, name="Engineering"
    )

    assert department.id is not None
    assert department.name == "Engineering"


@pytest.mark.asyncio
async def test_department_not_found_exception(db_session):
    with pytest.raises(NotFoundException) as exc_info:
        await department_service.get_department_by_id(db_session, 100)

    assert exc_info.value.detail == "Department does not exist"
