from fastapi import FastAPI
from middleware import configure_middleware
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

configure_middleware(app)

@app.get("/healthcheck", tags=["Health Check"])
def health_check():
    return "OK"

app.include_router(employee_router)
