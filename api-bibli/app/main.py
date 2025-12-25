from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.routers.author_router import router as author_router
from app.routers.book_router import router as book_router
from app.routers.loan_router import router as loan_router
from app.data.orm import engine, Base
from app.core.error_handlers import (
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    pass


apiVersion = "v1"

app = FastAPI(
    title="Library Management API",
    description="REST API for managing a modern library",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routes
app.include_router(author_router, prefix=f"/api/{apiVersion}")
app.include_router(book_router, prefix=f"/api/{apiVersion}")
app.include_router(loan_router, prefix=f"/api/{apiVersion}")
