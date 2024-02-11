from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, List
from fastapi import FastAPI, Depends, HTTPException, status

blogs = {
    "1": "FastAPI pre-requisite",
    "2": "Building APIs with FastAPI",
    "3": "Background Tasks | Celery x FastAPI"
}

users = {
    "8": 'Jamie',
    "9": "Roman"
}

app = FastAPI(title="Dependency Injection")


# function based dependency
def get_blog_or_404(blog_id: str):
    blog = blogs.get(blog_id)
    if not blog:
        raise HTTPException(detail=f"Blog with id: {blog_id} does not exist",
                            status_code=status.HTTP_404_NOT_FOUND)
    return blog


# parameterized dependency
class GetObjectOr404:
    def __init__(self, model: dict) -> None:
        self.model = model

    # This is what is going to make GetObjectOr404 callable
    def __call__(self, obj_id: str):
        obj = self.model.get(obj_id)
        if not obj:
            raise HTTPException(detail=f"Object with id: {obj_id} does not exist",
                                status_code=status.HTTP_404_NOT_FOUND)
        return obj


blog_dependency = GetObjectOr404(blogs)


@app.get("/blog/{blog_id}")
def get_blog(blog_name: str = Depends(blog_dependency)):
    # FastAPI takes care of evaluating the dependency by passing the ID to the dependency function
    # and injecting the returned value of the dependency function back to the variable blog_name!
    return blog_name


user_dependency = GetObjectOr404(users)


@app.get("/user/{user_id}")
def get_user(user_name: str = Depends(user_dependency)):
    # FastAPI takes care of evaluating the dependency by passing the ID to the dependency function
    # and injecting the returned value of the dependency function back to the variable blog_name!
    return user_name
