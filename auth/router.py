from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from auth import service
from auth.schema import TokenResponse, RefreshRequest
from db import get_db

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post("/login", response_model=TokenResponse)
async def login(
    body: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    tokens = await service.login(db=db, email=body.username, password=body.password)

    return {
        "token_type": "bearer",
        "access_token": tokens["access"],
        "refresh_token": tokens["refresh"],
    }


@auth_router.post("/refresh", response_model=TokenResponse)
async def refresh_access_token(body: RefreshRequest):
    tokens = await service.refresh_tokens(
        access_token=body.access_token, refresh_token=body.refresh_token
    )

    return {
        "token_type": "bearer",
        "access_token": tokens["access"],
        "refresh_token": tokens["refresh"],
    }
