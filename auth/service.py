from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from auth.repository import get_employee_by_email
from auth.utils import verify_password

from exceptions import UnauthorizedException


async def login(
    db: AsyncSession,
    email: str,
    password: str
) -> str:
    try:
        employee = await get_employee_by_email(db, email)

        if not verify_password(password, employee.password_hash):
            raise UnauthorizedException("Incorrect password for employee")

        return employee.get_access_token()
    except NoResultFound:
        raise UnauthorizedException("Employee does not exist")
