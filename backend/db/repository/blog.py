from db.models.blog import Blog
from db.schemas.blog import CreateBlog, UpdateBlog
# from db.schemas.blog import UpdateBlog
from sqlalchemy.orm import Session

# the repository will have the content to write the object to the database


def create_new_blog(blog_inp: CreateBlog, db_session: Session, author_id: int = 1):
    blog_out = Blog(title=blog_inp.title, slug=blog_inp.slug, content=blog_inp.content, author_id=author_id)
    # this is an instance of the Blog model
    db_session.add(blog_out)
    db_session.commit()
    db_session.refresh(blog_out)
    return blog_out


def retrieve_blog(blog_id=int, db_session=Session):
    blog_out = db_session.query(Blog).filter(Blog.id == blog_id).first()
    return blog_out


def list_blogs(db_session: Session):
    blog_list = db_session.query(Blog).filter(Blog.is_active == True).all()
    return blog_list


def update_blog_by_id(blog_id: int, blog: UpdateBlog, db_session: Session, author_id: int = 1):
    blog_in_db = db_session.query(Blog).filter(Blog.id == blog_id).first()
    if not blog_in_db:
        return {"error": f"Blog with id {blog_id} does not exist"}
    if not blog_in_db.author_id == author_id:
        return {"error": "Only the author can modify the blog"}
    blog_in_db.title = blog.title  # update with the title provided by the front end
    blog_in_db.content = blog.content if blog.content is not None else blog_in_db.content
    db_session.add(blog_in_db)
    db_session.commit()
    return blog_in_db


def delete_blog_by_id(blog_id: int, db_session: Session, author_id: int):
    blog_in_db = db_session.query(Blog).filter(Blog.id == blog_id)
    if not blog_in_db.first():
        return {"error": f"Could not find blog with id {blog_id}"}
    if not blog_in_db.first().author_id == author_id:
        return {"error": f"Only the author can delete a blog"}
    blog_in_db.delete()
    db_session.commit()
    return {"msg": f"Deleted blog with id {blog_id}"}
