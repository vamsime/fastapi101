import time

from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime as dt


class Language(str, Enum):
    PY = "python"
    JAVA = "Java"
    GP = "go"


class Comment(BaseModel):
    text_message: Optional[str] = None


class Blog(BaseModel):
    title: str = Field(min_length=5)  # this will raise a validation error if the minimum length condition is not met
    expected_users: int = Field(min_items=20, default=30)
    is_active: bool
    description: Optional[str] = None
    language: Language = Language.PY
    created_at: dt = Field(default_factory=dt.now)  # we need to import Field parameter from pydantic for dynamic inputs
    comments: Optional[List[Comment]]


b1 = Blog(title="Blog #1", is_active=False, comments=[{"text_message": None}, {"text_message": "first blog hmm!"}])
# is_active='up') => such an argument would through pydantic_core._pydantic_core.ValidationError!
b2 = Blog(title="Blog #2", is_active=False, description="just getting started with blog creation",
          comments=[{"text_message": None}])
b3 = Blog(title="Blog #3", is_active=False, description="started learning languages",
          comments=[{"text_message": None}])
time.sleep(5)
b4 = Blog(title="Blog #4", is_active=False, description="started learning languages",
          comments=[{"text_message": None}])

print(b1)
print(b2)
print(b3)
# all the above 3 will have been created at the samer time; while the fourth would have been created after the pause
# because of Field (& of course pause)
print(b4)
print(b4.json())
print(b4.dict())
print(b4.schema())
