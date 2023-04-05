
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Photo(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    url = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="photos")