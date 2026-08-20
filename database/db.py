from pymongo import AsyncMongoClient
from beanie import init_beanie
from environs import Env

from database.models import User

env = Env()
env.read_env()

client: AsyncMongoClient | None = None


async def connect_db() -> None:
    global client
    client = AsyncMongoClient(env.str("MONGO_URL"))
    await init_beanie(database=client.users, document_models=[User])


async def close_db() -> None:
    if client is not None:
        await client.close()  # у AsyncMongoClient close() тоже корутина