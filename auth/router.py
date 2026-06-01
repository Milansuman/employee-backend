from fastapi import APIRouter, Depends, Cookie
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from auth import service
from db import get_db
from exceptions import UnauthorizedException

auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@auth_router.post("/login")
async def login(body: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    tokens = await service.login(
        db=db,
        email=body.username,
        password=body.password
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
