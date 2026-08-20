from contextlib import asynccontextmanager
from fastapi import FastAPI
from user_routers import router as user_router

from database.db import connect_db, close_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await close_db()


app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
