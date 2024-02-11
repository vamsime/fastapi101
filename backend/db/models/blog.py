from datetime import datetime

from db.base_class import Base
from sqlalchemy import Boolean, Column, Integer, Text, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

# print("Blog imported")


class Blog(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    slug = Column(String, nullable=False, unique=True)
    content = Column(Text, nullable=True)
    author_id = Column(Integer, ForeignKey("user.id"))
    author = relationship("User", back_populates="blogs")
    created_at = Column(DateTime, default=datetime.now)
    is_active = Column(Boolean, default=False)
