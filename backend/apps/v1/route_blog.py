from fastapi import APIRouter, Request, Depends, Form, responses, status
from fastapi.templating import Jinja2Templates
from fastapi.security.utils import get_authorization_scheme_param
from sqlalchemy.orm import Session
from db.repository.blog import list_blogs, retrieve_blog, delete_blog, create_new_blog
from db.session import get_db
from db.schemas.blog import CreateBlog
from typing import Optional
from apis.v1.route_login import get_current_user


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


@router.get("/app/create-new-blog")
def create_blog(request: Request):
    return templates.TemplateResponse("blogs/create_blog.html", {"request": request})


@router.post("/app/create-new-blog")
def create_blog(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db),
):
    token = request.cookies.get("access_token")
    _, token = get_authorization_scheme_param(token)
    try:
        author = get_current_user(token=token, db_session=db)
        blog = CreateBlog(title=title, content=content)
        blog = create_new_blog(blog_inp=blog, db_session=db, author_id=author.id)
        return responses.RedirectResponse(
            "/?alert=Blog Submitted for Review", status_code=status.HTTP_302_FOUND
        )
    except Exception as e:
        errors = ["Please log in to create blog"]
        print("Exception raised", e)
        return templates.TemplateResponse(
            "blogs/create_blog.html",
            {"request": request, "errors": errors, "title": title, "content": content},
        )
