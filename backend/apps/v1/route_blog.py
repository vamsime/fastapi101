from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db.repository.blog import list_blogs, retrieve_blog
from db.session import get_db
from typing import Optional


# initialize an instance of the template
templates = Jinja2Templates(directory="templates")
router = APIRouter()


# if someone visits the home url, or the index url - FastAPI needs to serve this function;
#  which is why we are only giving / as argument
@router.get("/")
def home(req: Request, alert: Optional[str] = None, db_session: Session = Depends(get_db)):
    blogs = list_blogs(db_session)  # fetch the list of all the active blogs
    context_dictionary = {"request": req, 'blogs': blogs, "alert": alert}
    # pass the alert to the front end
    return templates.TemplateResponse("blogs/home.html", context_dictionary)
# 1) The FastAPI sends a request to this router
# 2) The home() gets executed which takes the request and parses it to home.html file
# 3) home.html inherits the base.html
# 4) takes the base.html and over-rides the blogs title & content


@router.get("/app/blog/{blog_id}")
def blog_detail(req: Request, blog_id: int, db_session: Session = Depends(get_db)):
    blog = retrieve_blog(blog_id=blog_id, db_session=db_session)
    context_dictionary = {"request": req, 'blog': blog}
    return templates.TemplateResponse("blogs/detail.html", context_dictionary)
