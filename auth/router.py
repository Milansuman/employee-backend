from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, Cookie
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from auth import service
from db import get_db
from env import env
from exceptions import UnauthorizedException

auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@auth_router.post("/login")
async def login(response: Response, body: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    tokens = await service.login(
        db=db,
        email=body.username,
        password=body.password
    )

    response.set_cookie(
        key="access",
        value=tokens["access"],
        httponly=True,
        secure=False,
        expires=datetime.now(timezone.utc) + timedelta(minutes=env.REFRESH_EXPIRY) #Access token needs to be available in order to refresh
    )

    response.set_cookie(
        key="refresh",
        value=tokens["refresh"],
        httponly=True,
        secure=False,
        expires=datetime.now(timezone.utc) + timedelta(minutes=env.REFRESH_EXPIRY)
    )

    return {
        "token_type": "bearer",
        "access_token": tokens["access"],
        "refresh_token": tokens["refresh"]
    }

@auth_router.post("/refresh")
async def refresh_access_token(response: Response, access: str | None = Cookie(default=None), refresh: str | None = Cookie(default=None)):
    try:
        tokens = await service.refresh_tokens(
            access_token=access,
            refresh_token=refresh
        )

        response.set_cookie(
            key="access",
            value=tokens["access"],
            httponly=True,
            secure=False,
            expires=datetime.now(timezone.utc) + timedelta(minutes=env.REFRESH_EXPIRY) #Access token needs to be available in order to refresh
        )

        response.set_cookie(
            key="refresh",
            value=tokens["refresh"],
            httponly=True,
            secure=False,
            expires=datetime.now(timezone.utc) + timedelta(minutes=env.REFRESH_EXPIRY)
        )

        return {
            "token_type": "bearer",
            "access_token": tokens["access"],
            "refresh_token": tokens["refresh"]
        }

    except UnauthorizedException as e:
        response.delete_cookie("access", httponly=True, secure=False)
        response.delete_cookie("refresh", httponly=True, secure=False)

        response.status_code = 401

        return {
            "detail": str(e)
        }
