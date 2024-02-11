from apis.v1 import route_blog
from apis.v1 import route_login
from apis.v1 import route_user
from fastapi import APIRouter

# the router will take the input being sent and pass it to the repository for the object to be stored in the database


api_router = APIRouter()
api_router.include_router(route_user.router, prefix="/users", tags=["users"])
api_router.include_router(route_blog.router, prefix="/blogs", tags=["blogs"])
api_router.include_router(route_login.router, prefix="", tags=["login"])

# we shall include this one single router inside the main.py
