from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers import books as books_router
from data.orm import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


apiVersion = "v1"
app = FastAPI(lifespan=lifespan)

app.include_router(books_router.router, prefix=f"/api/{apiVersion}")