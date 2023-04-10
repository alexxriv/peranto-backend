
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Photo(Base):
    photo_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256), index=True, nullable=False)
    description = Column(String(256), index=True, nullable=True)
    url = Column(String(256), nullable=False)
    owner_id = Column(String(10), ForeignKey("user.id"), nullable=False)
    owner = relationship("User", back_populates="photos")