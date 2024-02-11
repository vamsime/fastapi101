# base class which our user and blog would inherit
from typing import Any

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import as_declarative


@as_declarative()
class Base:
    id: Any
    __name__: str

    # to generate tablename from classname
    # should be mindful of the spell here; __tablename__ is syntax
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
