import json

# from apis.v1.route_login import authenticate_user
# from core.security import create_access_token
from db.repository.user import create_new_user
from db.session import get_db  # to get the single database session
from fastapi import APIRouter, Depends, Form, Request, responses, status
from fastapi.templating import Jinja2Templates
from pydantic.error_wrappers import ValidationError
from db.schemas.user import UserCreate  # to validate the data being sent by the front end
from db.schemas.user import ShowUser
from sqlalchemy.orm import Session


# templates = Jinja2Templates(directory="templates")
router = APIRouter()


# here we are using status to ensure we specify the right status code in the response
@router.post("/", response_model=ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(user_inp: UserCreate, db_session: Session = Depends(get_db)):
    user_out = create_new_user(user_inp=user_inp, db_session=db_session)
    return user_out


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
# @router.post("/login")
# def login(
#     request: Request,
#     email: str = Form(...),
#     password: str = Form(...),
#     db: Session = Depends(get_db),
# ):
#     errors = []
#     user = authenticate_user(email=email, password=password, db=db)
#     if not user:
#         errors.append("Incorrect email or password")
#         return templates.TemplateResponse(
#             "auth/login.html", {"request": request, "errors": errors}
#         )
#     access_token = create_access_token(data={"sub": email})
#     response = responses.RedirectResponse(
#         "/?alert=Successfully Logged In", status_code=status.HTTP_302_FOUND
#     )
#     response.set_cookie(
#         key="access_token", value=f"Bearer {access_token}", httponly=True
#     )
#     return response
