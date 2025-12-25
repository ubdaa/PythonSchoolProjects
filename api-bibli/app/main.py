from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.author_router import router as author_router
from routers.book_router import router as book_router
from routers.loan_router import router as loan_router
from data.orm import engine, Base


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
