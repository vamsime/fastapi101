import os
import sys
from typing import Any
from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# this is to include backend dir in sys.path so that we can import from db,main.py

# this is the file that pytest will be looking for

from db.base import Base
from db.session import get_db
from apis.base import api_router


def start_application():
    """
    This creates the instance of FastAPI, includes the necessary router and returns the app instance
    """
    app = FastAPI()
    app.include_router(api_router)
    return app


# this section is related to the configuration of SQLite database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# Use connect_args parameter only with sqlite
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
# fixtures are functions that run before each test function to which it is applied
# they are used to feed some data to the test
# instead of running the same code for every test, we can just attach the fixture function to the test!
#       and it will run & return the data for each of the tests
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    Base.metadata.create_all(engine)  # Create the tables in the database
    _app = start_application()
    yield _app  # starting and yielding an instance of the application
    Base.metadata.drop_all(engine)  # drop the tables when the test concludes


@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    """
    This function takes care of connecting with the database, yielding a session and rollback the transaction when
    the test concludes
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session  # use the session in tests.
    session.close()
    transaction.rollback()
    connection.close()


# In this function, we are taking the app instance, the db session and over-riding the dependency get_db and
# giving the connection to SQLite db
@pytest.fixture(scope="function")
def client(
    app: FastAPI, db_session: SessionTesting
) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client
