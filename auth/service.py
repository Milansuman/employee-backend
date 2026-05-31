from datetime import datetime, timezone

import jwt
from jwt.exceptions import DecodeError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from auth.repository import get_employee_by_email
from auth.utils import verify_password, create_jwt
from env import env

from exceptions import BadRequestException, UnauthorizedException

async def login(
    db: AsyncSession,
    email: str,
    password: str
) -> dict:
    try:
        employee = await get_employee_by_email(db, email)

        if not verify_password(password, employee.password_hash):
            raise UnauthorizedException("Incorrect password for employee")

        claims = {
            "id": employee.id,
            "name": employee.name
        }

        access_token = create_jwt(claims, env.JWT_SECRET, env.TOKEN_EXPIRY)
        refresh_token = create_jwt({
            "token": access_token
        }, env.JWT_SECRET, env.REFRESH_EXPIRY)

        return {
            "access": access_token,
            "refresh": refresh_token
        }
    except NoResultFound:
        raise UnauthorizedException("Employee does not exist")

async def refresh_tokens(
    access_token: str | None,
    refresh_token: str | None
):
    if not access_token or not refresh_token:
        raise BadRequestException("Required tokens not present")

    try:
        access_claims = jwt.decode(access_token, env.JWT_SECRET, algorithms=[env.JWT_ALGORITHM])
        refresh_claims = jwt.decode(refresh_token, env.JWT_SECRET, algorithms=[env.JWT_ALGORITHM])

        if refresh_claims["exp"] < datetime.now(timezone.utc).timestamp():
            raise UnauthorizedException("Expired refresh token")

        if refresh_claims["claims"]["token"] != access_token:
            raise UnauthorizedException("Used refresh token")

        new_access_token = create_jwt(access_claims, env.JWT_SECRET, env.TOKEN_EXPIRY)
        new_refresh_token = create_jwt({
            "token": new_access_token
        }, env.JWT_SECRET, env.REFRESH_EXPIRY)

        return {
            "access": new_access_token,
            "refresh": new_refresh_token
        }
    except DecodeError:
        raise UnauthorizedException("Invalid tokens")
