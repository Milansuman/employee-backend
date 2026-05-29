from fastapi import FastAPI
from middleware import configure_middleware
import logging
import uvicorn
from lifespan import lifespan

from employees.router import employee_router

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

def main():
    uvicorn.run(
        app="main:app",
        reload=True
    )

if __name__ == "__main__":
    main()
