import pytest
from testcontainers.community.mongodb import MongoDbContainer
from pymongo import AsyncMongoClient
from beanie import init_beanie
from main import app
from httpx import AsyncClient, ASGITransport

from database.models import User  # мои Document-модели


### === Настройка для тестов, используем настоящую БД в тестовом контейнере === ###

# Общий паттерн
@pytest.fixture(scope="session")
def mongo_container():
    '''Поднимаем 1 раз на сессию, чтобы не дублировать контейнер'''
    with MongoDbContainer("mongo:latest") as mongo:
        yield mongo


@pytest.fixture
async def db(mongo_container):
    '''Подключаемся к тестовому контейнеру, удаляем БД в конце теста'''
    client = AsyncMongoClient(mongo_container.get_connection_url())
    db_name = "test_db"

    await init_beanie(
        database=client[db_name], # подключаемся к созданному контейнеру и создаем БД
          document_models=[User] # и мои Document-модели
          )

    yield client[db_name]
    await client.drop_database(db_name) # у MongoDB нет откатов, проще дропнуть всю таблицу между тестами
    await client.close()


@pytest.fixture
async def app_client(db):
    '''Тестовый клиент FastAPI'''
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client