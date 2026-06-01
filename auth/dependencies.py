import jwt
from jwt.exceptions import DecodeError, ExpiredSignatureError
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from employees import service as employee_service
from exceptions import ForbiddenException, UnauthorizedException
from env import env
from db import get_db
from models.employee import Employee, EmployeeRoles

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", refreshUrl="/auth/refresh")


def verify_access_token(access: str = Depends(oauth2_scheme)):
    if not access:
        raise UnauthorizedException("Employee has not logged in")

    try:
        jwt.decode(access, env.JWT_SECRET, algorithms=[env.JWT_ALGORITHM])
    except DecodeError:
        raise UnauthorizedException("Invalid token")

    except ExpiredSignatureError:
        raise UnauthorizedException("Token expired")


async def get_current_user(
    access: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
):
    if not access:
        raise UnauthorizedException("Employee has not logged in")

    try:
        claims = jwt.decode(access, env.JWT_SECRET, algorithms=[env.JWT_ALGORITHM])

        employee = await employee_service.get_by_id(db, claims["claims"]["id"])

        return employee
    except DecodeError:
        raise UnauthorizedException("Invalid token")

    except ExpiredSignatureError:
        raise UnauthorizedException("Token expired")


def require_roles(roles: list[EmployeeRoles]):

    async def _require_role(employee: Employee = Depends(get_current_user)):
        if employee.role in roles:
            raise ForbiddenException("Access denied to role")

    return _require_role
