from contextlib import asynccontextmanager
from db import create_tables
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield
