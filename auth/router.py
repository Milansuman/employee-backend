import logging
from fastapi import APIRouter, Depends, Cookie
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from auth import service
from auth.schema import TokenResponse
from db import get_db

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

logger = logging.getLogger(__name__)

@auth_router.post("/login", response_model=TokenResponse)
async def login(
    body: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    tokens = await service.login(db=db, email=body.username, password=body.password)

    logger.info(f"{body.username} logged in successfully")

    return {
        "token_type": "bearer",
        "access_token": tokens["access"],
        "refresh_token": tokens["refresh"],
    }


@auth_router.post("/refresh", response_model=TokenResponse)
async def refresh_access_token(
    response: Response,
    access: str | None = Cookie(default=None),
    refresh: str | None = Cookie(default=None),
):
    tokens = await service.refresh_tokens(
        access_token=access, refresh_token=refresh
    )

    return {
        "token_type": "bearer",
        "access_token": tokens["access"],
        "refresh_token": tokens["refresh"],
    }
