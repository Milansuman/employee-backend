from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from middleware.logger import RequestLoggingMiddleware
import logging
from lifespan import lifespan

from routers import employee_router

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

app.include_router(employee_router)
