from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, List
from datetime import datetime as dt


class CreateUser(BaseModel):
    email: str
    password: str
    confirm_password: str

    @field_validator("email")
    def validate_email(cls, value):
        if "admin" in value:
            raise ValueError("This email is not allowed!")

    @model_validator(mode='after')
    def validate_password(cls, values):
        password = values.password
        confirm_password = values.confirm_password
        if password != confirm_password:
            raise ValueError("The two passwords should match!")
        return values


# email="bingadmin@fastapitutorial.com" should raise a ValueError
# password="123", confirm_password="1234" should raise a ValueError
CreateUser(email="bing@fastapitutorial.com", password="123",
           confirm_password="123")
