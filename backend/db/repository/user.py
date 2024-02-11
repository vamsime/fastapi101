from core.hashing import Hasher
from db.models.user import User  # to create an instance of User model that will be stored in the db table
from db.schemas.user import UserCreate
from sqlalchemy.orm import Session


def create_new_user(user_inp: UserCreate, db_session: Session):
    """
    takes arguments of type UserCreate and a database session
    """
    # instance of user object
    user_out = User(
        email=user_inp.email,
        password=Hasher.get_password_hash(user_inp.password),
        is_active=True,
        is_superuser=False,
    )
    db_session.add(user_out)
    db_session.commit()  # since we have set auto_commit as False, just adding won't suffice
    db_session.refresh(user_out)  # refresh the attributes on the given instance
    return user_out
