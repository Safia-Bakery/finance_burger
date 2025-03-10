import os
import sys

import pytest_asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import asyncio
import asyncpg
import pytest
from typing import Generator, Any, AsyncGenerator
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

from core.config import TEST_DB_URL, TEST_SQLALCHEMY_URL
from core.session import get_db
from main import app


test_engine = create_async_engine(TEST_DB_URL, future=True, echo=True)
test_async_session = sessionmaker(bind=test_engine, expire_on_commit=False, class_=AsyncSession)


if TEST_DB_URL is None:
    raise ValueError("TEST_DB_URL environment variable is not found")


CLEAN_TABLES = [
    "users",
]


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    # loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def run_migrations():
    os.system('alembic init migrations')
    os.system('alembic revision --autogenerate -m "test running migrations"')
    os.system('alembic upgrade heads')


@pytest.fixture(scope="session")
async def async_session_test():
    engine = create_async_engine(TEST_DB_URL, future=True, echo=True)
    async_session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
    yield async_session



async def table_exists(session: AsyncSession, table_name: str) -> bool:
    """Check if a table exists in the database."""
    result = await session.execute(
        f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{table_name}');"
    )
    return result.scalar()


@pytest.fixture(scope="function", autouse=True)
async def clean_tables(async_session_test):
    async with async_session_test() as session:
        async with session.begin():
            for table in CLEAN_TABLES:
                if await table_exists(session, table):
                    await session.execute(f"""TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;""")


async def _get_test_db():
    try:
        yield test_async_session()
    finally:
        pass


@pytest.fixture(scope="function")
async def client() -> AsyncGenerator[AsyncClient, None]:

    app.dependency_overrides[get_db] = _get_test_db

    async with AsyncClient(app=app, base_url="http://localhost") as client:
        yield client


@pytest.fixture(scope="session")
async def asyncpg_pool():
    pool = await asyncpg.create_pool(TEST_SQLALCHEMY_URL)
    yield pool
    await pool.close()


@pytest.fixture
async def get_user_from_database(asyncpg_pool):

    async def get_user_from_database_by_id(user_id: str):
        async with asyncpg_pool.acquire() as connection:
            return await connection.fetch(f"""SELECT * FROM users WHERE id = $1;""", user_id)

    return get_user_from_database_by_id

