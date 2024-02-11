import json

# from core.security import create_access_token
from db.repository.blog import create_new_blog, retrieve_blog, list_blogs, update_blog_by_id, delete_blog_by_id
from db.session import get_db  # to get the single database session
from fastapi import APIRouter, Depends, Form, Request, responses, status, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic.error_wrappers import ValidationError
from db.schemas.blog import CreateBlog  # to validate the data being sent by the front end
from db.schemas.blog import ShowBlog, UpdateBlog
from db.models.user import User
from apis.v1.route_login import get_current_user
from sqlalchemy.orm import Session
from typing import List


# templates = Jinja2Templates(directory="templates")
router = APIRouter()


# here we are using status to ensure we specify the right status code in the response
@router.post("/", response_model=ShowBlog, status_code=status.HTTP_201_CREATED)
def create_blog(blog_inp: CreateBlog,
                db_session: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    blog_out = create_new_blog(blog_inp=blog_inp, db_session=db_session, author_id=current_user.id)
    return blog_out


# here we are using status to ensure we specify the right status code in the response
@router.get("/{blog_id}", response_model=ShowBlog)
def get_blog(blog_id: int, db_session: Session = Depends(get_db)):
    blog_out = retrieve_blog(blog_id=blog_id, db_session=db_session)
    if not blog_out:
        raise HTTPException(detail=f"Blog with id {blog_id} does not exist",
                            status_code=status.HTTP_404_NOT_FOUND)
    return blog_out


# Let us now create the url end-point that gives us a list of active blogs
# Since we already have a prefix, we need not give any here
@router.get("", response_model=List[ShowBlog])
def get_all_blogs(db_session: Session = Depends(get_db)):
    blog_list = list_blogs(db_session=db_session)
    return blog_list


# Let us now build a route that will support us in updating a blog
@router.get("", response_model=List[ShowBlog])
def get_all_blogs(db_session: Session = Depends(get_db)):
    blog_list = list_blogs(db_session=db_session)
    return blog_list


# Let us now build a route that will support us in updating a blog
@router.put("/{blog_id}", response_model=ShowBlog)
def update_a_blog(blog_id: int, blog: UpdateBlog,
                  db_session: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    # The blog information here is what we get from the front end or the postman
    blog_out = update_blog_by_id(blog_id=blog_id, blog=blog, db_session=db_session, author_id=current_user.id)
    if isinstance(blog_out, dict):
        raise HTTPException(detail=blog_out.get("error"), status_code=status.HTTP_400_BAD_REQUEST)
    # if not blog_out:
    #     raise HTTPException(detail=f"Blog with id: {blog_id} does not seem to exist!")
    return blog_out


# Let us now build a route that will help us in deleting a blog, by using its ID
# Remember. if we try to show a response model of ShowBlog - then we would get an error considering we won't have
# the blog anymore!
@router.delete("/{blog_id}")
def delete_a_blog(blog_id: int,
                  db_session: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    msg_txt = delete_blog_by_id(blog_id=blog_id, db_session=db_session, author_id=current_user.id)
    if msg_txt.get("error"):
        raise HTTPException(detail=msg_txt.get("error"), status_code=status.HTTP_400_BAD_REQUEST)
    return {"msg": msg_txt.get("msg")}


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
