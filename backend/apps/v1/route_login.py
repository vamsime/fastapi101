from fastapi import APIRouter, Request, Depends, responses, status, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import json
from db.session import get_db
from db.schemas.user import UserCreate  # UserCreate schema to validate the email and password being sent
from db.repository.user import create_new_user
from pydantic.error_wrappers import ValidationError  # to catch the error serve our own code


# initialize an instance of the template
templates = Jinja2Templates(directory="templates")
router = APIRouter()


# if someone visits the home url, or the index url - FastAPI needs to serve this function;
#  which is why we are only giving / as argument
@router.get("/register")
def register(req: Request, db_session: Session = Depends(get_db)):
    context_dictionary = {'request': req}
    return templates.TemplateResponse("auth/register.html", context_dictionary)
# 1) The FastAPI sends a request to this router
# 2) The home() gets executed which takes the request and parses it to home.html file
# 3) home.html inherits the base.html
# 4) takes the base.html and over-rides the blogs title & content

@router.post("/register")
def register(req: Request,
             email: str = Form(...),
             password: str = Form(...),
             db_session: Session = Depends(get_db)):
    """
    ... makes the argument mandatory
    """
    errors = []
    try:
        user = UserCreate(email=email, password=password)
        create_new_user(user_inp = user, db_session = db_session)
        return responses.RedirectResponse("?alert=Successfully%20Registered",
                                          status_code=status.HTTP_302_FOUND, )
        # status.HTTP_302_FOUND to mention that it is a get redirect; otherwise FastAPI would
        # think that it is a post redirect
    except ValidationError as e:
        errors_list = json.loads(e.json())
        for itm in errors_list:
            errors.append(itm.get("loc")[0] + ": " + itm.get("msg"))
        return templates.TemplateResponse("auth/register.html",
                                          {'request': req, "errors": errors})



