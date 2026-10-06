import os
import shutil

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db


# ============================================================
# TEST DATABASE
# ============================================================

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+psycopg://postgres:12345@localhost:5432/secure_backend_test"
)


test_engine = create_engine(
    TEST_DATABASE_URL,
    pool_pre_ping=True
)


TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


# ============================================================
# CREATE TEST DATABASE TABLES
# ============================================================

@pytest.fixture(
    scope="session",
    autouse=True
)
def create_test_database_tables():

    Base.metadata.create_all(
        bind=test_engine
    )

    yield

    Base.metadata.drop_all(
        bind=test_engine
    )


# ============================================================
# DATABASE FIXTURE
# ============================================================

@pytest.fixture
def db():

    connection = test_engine.connect()

    transaction = connection.begin()

    session = TestingSessionLocal(
        bind=connection
    )

    try:
        yield session

    finally:
        session.close()
        transaction.rollback()
        connection.close()


# ============================================================
# UPLOAD FOLDER CLEANUP
# ============================================================

@pytest.fixture(autouse=True)
def cleanup_uploads():

    upload_dir = "uploads"

    os.makedirs(
        upload_dir,
        exist_ok=True
    )

    # Remove old files before each test
    for filename in os.listdir(upload_dir):

        file_path = os.path.join(
            upload_dir,
            filename
        )

        if os.path.isfile(file_path):
            os.remove(file_path)

        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

    yield

    # Remove files after each test
    for filename in os.listdir(upload_dir):

        file_path = os.path.join(
            upload_dir,
            filename
        )

        if os.path.isfile(file_path):
            os.remove(file_path)

        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)


# ============================================================
# FASTAPI TEST CLIENT
# ============================================================

@pytest.fixture
def client(db):

    def override_get_db():

        try:
            yield db

        finally:
            pass

    # Replace application's DB with test DB
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    # IMPORTANT:
    # Remove the test database override
    # after each test.
    app.dependency_overrides.clear()