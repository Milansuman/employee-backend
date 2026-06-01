from datetime import datetime, timezone
import jwt
from jwt.exceptions import DecodeError
from fastapi import Cookie, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from employees import service as employee_service
from exceptions import UnauthorizedException
from env import env
from db import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", refreshUrl="/auth/refresh")

def verify_access_token_cookie(access: str | None = Cookie(default=None)):
    if not access:
        raise UnauthorizedException("Employee has not logged in")

    try:
        claims = jwt.decode(access, env.JWT_SECRET, algorithms=[env.JWT_ALGORITHM])

        if claims["exp"] < datetime.now(timezone.utc).timestamp():
            raise UnauthorizedException("Token expired")

    except DecodeError:
        raise UnauthorizedException("Invalid token")

async def get_current_user_oauth(access: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    if not access:
        raise UnauthorizedException("Employee has not logged in")

    try:
        print(access)
        claims = jwt.decode(access, env.JWT_SECRET, algorithms=[env.JWT_ALGORITHM])

        if claims["exp"] < datetime.now(timezone.utc).timestamp():
            raise UnauthorizedException("Token expired")

        employee = await employee_service.get_by_id(db, claims["claims"]["id"])

        return employee
    except DecodeError:
        raise UnauthorizedException("Invalid token")
