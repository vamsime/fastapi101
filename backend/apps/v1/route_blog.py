from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


# initialize an instance of the template
templates = Jinja2Templates(directory="templates")
router = APIRouter()


# if someone visits the home url, or the index url - FastAPI needs to serve this function;
#  which is why we are only giving / as argument
@router.get("/")
def home(req: Request):
    print(dir(req))
    return templates.TemplateResponse("blogs/home.html", {"request": req})
# 1) The FastAPI sends a request to this router
# 2) The home() gets executed which takes the request and parses it to home.html file
# 3) home.html inherits the base.html
# 4) takes the base.html and over-rides the blogs title & content

