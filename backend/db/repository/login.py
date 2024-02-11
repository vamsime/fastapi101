from db.models.user import User
from sqlalchemy.orm import Session


def get_user_by_email(email_inp=str, db_session=Session):
    user = db_session.query(User).filter(User.email == email_inp).first()
    return user
