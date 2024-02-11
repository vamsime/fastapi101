from datetime import datetime, timedelta
from typing import Optional
from core.config import settings
from jose import jwt


def create_access_token(data_arg: dict, expires_delta: Optional[timedelta] = None):
    """
    This will get an argument of type dictionary that will contain the payload the needs to be encoded
    """
    to_encode = data_arg.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt

# the above can be validated easily in a python shell
# python
# from core.security import create_access_token
# inp_data = {"sub": "ping@fastapitutorial.com"}
# create_access_token(data_arg=inp_data)
# copy the token
# go to website: jwt.io
# and validate
#


