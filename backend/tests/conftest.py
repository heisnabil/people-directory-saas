"""
Pytest fixtures for backend tests.

Uses an in-memory SQLite database to avoid requiring MySQL for test runs.
Overrides FastAPI's get_db dependency to inject the test session.
"""

from datetime import date
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models.employee import Employee

# In-memory SQLite for fast, isolated tests
SQLALCHEMY_TEST_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_TEST_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


@pytest.fixture(autouse=True)
def setup_database() -> Generator[None, None, None]:
    """Create all tables before each test, drop after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    """Provide a clean database session for each test."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db_session: Session) -> TestClient:
    """
    FastAPI TestClient with the test database injected.

    Overrides the get_db dependency so all requests use the test session
    instead of the real MySQL connection.
    """

    def _override_get_db() -> Generator[Session, None, None]:
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def seeded_db(db_session: Session) -> Session:
    """Seed the test database with representative employee data."""
    employees = [
        Employee(
            name="Rahul Sharma",
            email="rahul.sharma@test.com",
            department="Engineering",
            designation="Senior Software Engineer",
            date_of_joining=date(2021, 3, 15),
        ),
        Employee(
            name="Priya Patel",
            email="priya.patel@test.com",
            department="Engineering",
            designation="Frontend Developer",
            date_of_joining=date(2022, 7, 1),
        ),
        Employee(
            name="Amit Kumar",
            email="amit.kumar@test.com",
            department="Product",
            designation="Product Manager",
            date_of_joining=date(2020, 11, 10),
        ),
        Employee(
            name="Sneha Reddy",
            email="sneha.reddy@test.com",
            department="Design",
            designation="UI/UX Designer",
            date_of_joining=date(2023, 1, 20),
        ),
        Employee(
            name="Vikram Singh",
            email="vikram.singh@test.com",
            department="Engineering",
            designation="DevOps Engineer",
            date_of_joining=date(2021, 9, 5),
        ),
    ]
    db_session.add_all(employees)
    db_session.commit()
    return db_session
