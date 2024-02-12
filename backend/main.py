from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from core.config import settings
from db.session import engine
from apis.base import api_router
from apps.base import app_router


def include_router(app_inp):
    app_inp.include_router(api_router)
    app_inp.include_router(app_router)


# StaticFiles need to configured by mounting the static directory
def configure_staticfiles(app_inp):
    app_inp.mount("/static", StaticFiles(directory="static"), name="static")


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
    configure_staticfiles(local_app)
    return local_app


app = start_application()


@app.get("/About")
def hello():
    return {"message": "Hello FastAPI🚀"}

