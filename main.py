from typing import Annotated

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from middleware.logger import RequestLoggingMiddleware
from repositories.employee import (
    create_employee as add_employee,
    delete_employee as remove_employee,
    get_all_employees,
    get_employee_by_id,
    update_employee as update_employee_by_id
)
from schema.employee import CreateEmployee, Employee
import logging
from lifespan import lifespan
from asyncpg.exceptions import UniqueViolationError
from sqlalchemy.exc import NoResultFound

logging.basicConfig(
    level=logging.INFO
)

app = FastAPI(
    title="Employee API",
    description="A simple crud api",
    lifespan=lifespan
)

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/healthcheck", tags=["Health Check"])
def health_check():
    return "OK"

@app.get("/employee/all", tags=["Employee"])
async def all_employees(db: Annotated[AsyncSession, Depends(get_db)]):
    return await get_all_employees(db)

@app.get("/employee/{id}", tags=["Employee"])
async def get_employee(id: int, response: Response, db: Annotated[AsyncSession, Depends(get_db)]):
    try:
        return await get_employee_by_id(db, id)
    except NoResultFound:
        response.status_code = 404
        return {
            "detail": "Employee not found"
        }

@app.post("/employee", tags=["Employee"])
async def create_employee(body: CreateEmployee, response: Response, db: Annotated[AsyncSession, Depends(get_db)]):
    try:
        employee = await add_employee(db, body) #type: ignore
        return employee
    except UniqueViolationError:
        response.status_code = 400
        return {
            "error": "Employee already exists"
        }

@app.patch("/employee/{id}", tags=["Employee"])
async def update_employee(id: int, body: CreateEmployee, response: Response, db: Annotated[AsyncSession, Depends(get_db)]):
    try:
        employee = await update_employee_by_id(db, {
            "id": id,
            "name": body["name"],
            "email": body["email"],
            "phone": body["phone"],
            "address": body["address"]
        })

        return employee
    except NoResultFound:
        response.status_code = 400
        return {
            "error": "Employee does not exist"
        }
    except UniqueViolationError:
        response.status_code = 400
        return {
            "error": "Email is already in use"
        }


@app.delete("/employee/{id}", tags=["Employee"])
async def delete_employee(id: int, response: Response, db: Annotated[AsyncSession, Depends(get_db)]):
    try:
        await remove_employee(db, id)
    except NoResultFound:
        response.status_code = 400
        return {
            "error": "Employee does not exist"
        }
