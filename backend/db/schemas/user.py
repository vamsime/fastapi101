from pydantic import BaseModel, EmailStr, Field


# properties required during user creation
class UserCreate(BaseModel):
    """Whenever the user tries to register, this will validate the data sent by those users
    We inherit the BaseModel because it empowers us to suggest validation errors to the users"""
    email: EmailStr
    password: str = Field(..., min_length=4)

# the above can be validated easily in a python shell
# python -> from db.schemas.user import UserCreate
# UserCreate(email="ping#fastapitutorial.com", password="123")


class ShowUser(BaseModel):
    """
    This will be responsible for showing the fields in the response
    """
    id: int
    email: EmailStr
    is_active: bool

    class Config:  # tells pydantic to convert even non dict obj to json
        orm_mode = True
        # we specify orm_mode as True because the user response from the api is not dict but sqlalchemy orm object
