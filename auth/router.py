from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from auth import service
from db import get_db
from auth.schema import LoginAttempt

auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@auth_router.post("/login")
async def login(body: LoginAttempt, response: Response, db: AsyncSession = Depends(get_db)):
    access_token = await service.login(
        db=db,
        email=body.email,
        password=body.password
    )

    response.set_cookie(
        key="auth",
        value=access_token,
        httponly=True,
        secure=False
    )

    return {
        "detail": "success"
    }
