import os

import pytest
from alembic import command
from alembic.config import Config
from dotenv import load_dotenv
from sqlalchemy import create_engine, make_url
from sqlalchemy.orm import sessionmaker

from src.config.settings import settings


def get_test_connection_string() -> str:
    database_uri: str = settings.TEST_DATABASE_URI
    if not database_uri:
        load_dotenv()
        database_uri = os.getenv("TEST_DATABASE_URI", "")
    return database_uri

test_connection_string = get_test_connection_string()
test_db_url = make_url(test_connection_string)

if "test" not in (test_db_url.database or ""):
    raise RuntimeError(
        f"{test_db_url.database} does not look like test URL.... stopping...."
    )

engine = create_engine(
    test_connection_string,
    future=True,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True,
)

def run_migrations():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", test_connection_string)
    command.upgrade(alembic_cfg, "head")


def downgrade_all():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", test_connection_string)
    command.downgrade(alembic_cfg, "base")


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    run_migrations()
    yield
    downgrade_all()

@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()