from fastapi import FastAPI
from core.config import settings
from db.session import engine
# from db.base import Base
from apis.base import api_router


def include_router(app_inp):
    app_inp.include_router(api_router)


def create_tables():
    """We shall use this only when we are not using alembic for the migration"""
    print("create_tables() called")
    # Base.metadata.create_all(bind=engine)
    # this way, every time any model that inherits the Base class, they will be auto-created
    # once the app is starting up


def start_application():
    local_app = FastAPI(title=settings.PROJECT_TITLE, version=settings.PROJECT_VERSION)
    # create_tables()
    # This is done to create the db migrations only by alembic
    include_router(local_app)
    return local_app


app = start_application()


@app.get("/")
def hello():
    return {"message": "Hello FastAPI🚀"}
