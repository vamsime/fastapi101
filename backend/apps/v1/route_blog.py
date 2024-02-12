from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db.repository.blog import list_blogs
from db.session import get_db


# initialize an instance of the template
templates = Jinja2Templates(directory="templates")
router = APIRouter()


# if someone visits the home url, or the index url - FastAPI needs to serve this function;
#  which is why we are only giving / as argument
@router.get("/")
def home(req: Request, db_session: Session = Depends(get_db)):
    blogs = list_blogs(db_session)  # fetch the list of all the active blogs
    context_dictionary = {"request": req, 'blogs': blogs}
    return templates.TemplateResponse("blogs/home.html", context_dictionary)
# 1) The FastAPI sends a request to this router
# 2) The home() gets executed which takes the request and parses it to home.html file
# 3) home.html inherits the base.html
# 4) takes the base.html and over-rides the blogs title & content

