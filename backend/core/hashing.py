from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# the argument schemes means the hashing algorithm that we want to use


class Hasher:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)

# the above can be validated easily in a python shell
# python
# from core.hashing import Hasher
# Hasher.get_password_hash("supersecret")
# Hasher.verify_password("super", <the above value>)
# Hasher.verify_password("supersecret", <the above value>)
#
