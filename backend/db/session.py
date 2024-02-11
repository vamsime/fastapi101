from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
from core.config import settings

SQLALCHEMY_DB_URL = settings.DATABASE_URL
print("Database URL is ", SQLALCHEMY_DB_URL)
engine = create_engine(SQLALCHEMY_DB_URL)


# SQLALCHEMY_DB_URL = "sqlite:///./sql_app.db"
# engine = create_engine(SQLALCHEMY_DB_URL, connect_args={"check_same_thread": False})
# # This argument is necessary because sqlite cannot handle multiple threads

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
# this session_local can be thought of as a set of sessions
# an instance of this would give a db session which we can use to query the db


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# the above can be validated easily in a python shell
# python
# from db.models.user import User
# from db.models.blog import Blog
# from db.session import get_db
# db = get_db().__next__()
#       .__next__() should be used to yield the session
# db
# db.query(User).all()
# db.query(Blog).all()
