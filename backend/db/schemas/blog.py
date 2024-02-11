from datetime import datetime
from typing import Optional

from pydantic import BaseModel, root_validator

# the schema will validate the input being sent to the api


class CreateBlog(BaseModel):
    """
    Will take in the input being sent to the api and validate it
    """
    title: str
    slug: Optional[str]
    content: Optional[str] = None

    @root_validator(pre=True)  # we want to take the input and generate the slug dynamically if the title is provided!
    def generate_slug(cls, values):
        # values will be the dictionary of the input being sent
        if "title" in values:
            values["slug"] = values.get("title").replace(" ", "-").lower()
        return values


class UpdateBlog(CreateBlog):
    # This essentially has to the same thing as the parent class!
    pass


class ShowBlog(BaseModel):
    """
    We will use this to filter the keys being sent in response
    """
    title: str
    content: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True
