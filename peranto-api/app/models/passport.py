from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Passport(Base):
    id = Column(Integer, primary_key=True, index=True)
    passport_type = Column(String(256), nullable=False)
    country_code = Column(String(256), index=True, nullable=True)
    passport_number = Column(String(256), nullable=True)
    last_names = Column(String(256), nullable=True)
    names = Column(String(256), nullable=True)
    country = Column(String(256), nullable=True)
    curp = Column(String(256), nullable=True)
    birth_date = Column(String(256), nullable=True)
    issue_date = Column(String(256), nullable=True)
    expiration_date = Column(String(256), nullable=True)
    owner_id = Column(Integer, ForeignKey("user.id"), nullable=True, unique=True)
    owner = relationship("User", back_populates="passport")
