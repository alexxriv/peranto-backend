from sqlalchemy import Integer, String, Column, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    is_superuser = Column(Boolean(), default=False)


    photos = relationship(
        "Photo",
        cascade="all,delete-orphan",
        back_populates="submitter",
        uselist=True)
    
    hashed_password = Column(String(100), nullable=False)

