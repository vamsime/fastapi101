import json

from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from core.security import create_access_token
from core.config import settings
# OAuth2PasswordRequestForm asks for username and password;
from core.hashing import Hasher
from db.repository.user import create_new_user
from db.repository.login import get_user_by_email
from db.session import get_db
from fastapi import APIRouter, Depends, Form, Request, responses, status, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic.error_wrappers import ValidationError
from db.schemas.user import UserCreate
from sqlalchemy.orm import Session


templates = Jinja2Templates(directory="templates")
router = APIRouter()


def authenticate_user(email_inp: str, password_inp: str, db_session: Session):
    user = get_user_by_email(email_inp=email_inp, db_session=db_session)
    print(user)
    if not user:
        return False
    if not Hasher.verify_password(password_inp, user.password):
        return False
    return user


@router.post("/token")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(get_db),
):
    errors = []
    user = authenticate_user(email_inp=form_data.username, password_inp=form_data.password, db_session=db_session)
    if not user:
        raise HTTPException(detail="Incorrect email or password", status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = create_access_token(data_arg={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
# this is going to be the url to which we can supply username and password & get the password
# This helps in creating the button in the api documentation


def get_current_user(token: str = Depends(oauth2_scheme), db_session: Session = Depends(get_db)):
    """
    This ia utility function which when provided the token will validate whether the token is valid or not
    and returns the user in case the token is valid
    We will use this as a dependency function in our route; takes the token from the request,
    validate it and provide us the user corresponding to that token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials; Please login again"
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(email_inp=email, db_session=db_session)
    if user is None:
        raise credentials_exception
    return user


# @router.get("/register")
# def register(request: Request):
#     return templates.TemplateResponse("auth/register.html", {"request": request})
#
#
# @router.post("/register")
# def register(
#     request: Request,
#     email: str = Form(...),
#     password: str = Form(...),
#     db: Session = Depends(get_db),
# ):
#     errors = []
#     try:
#         user = UserCreate(email=email, password=password)
#         create_new_user(user=user, db=db)
#         return responses.RedirectResponse(
#             "/?alert=Successfully%20Registered", status_code=status.HTTP_302_FOUND
#         )
#     except ValidationError as e:
#         errors_list = json.loads(e.json())
#         for item in errors_list:
#             errors.append(item.get("loc")[0] + ": " + item.get("msg"))
#         return templates.TemplateResponse(
#             "auth/register.html", {"request": request, "errors": errors}
#         )
#
#
# @router.get("/login")
# def login(request: Request):
#     return templates.TemplateResponse("auth/login.html", {"request": request})
#
#

