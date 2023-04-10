from typing import Optional

from pydantic import BaseModel, EmailStr, HttpUrl


class PhotoBase(BaseModel):
    title: str
    description: Optional[str]
    url: HttpUrl



# Properties to receive via API on creation
class PhotoCreate(PhotoBase):
    owner_id: int


# Properties to receive via API on update
class PhotoUpdate(PhotoBase):
    url: Optional[HttpUrl]


class PhotoInDBBase(PhotoBase):
    photo_id: int
    owner_id: int

    class Config: # This orm_mode is required to allow Pydantic to read the data even if it is not a dict, but an ORM model. Without it if you return a SQLAlchemy model from your path operation it wouldnt include the relationship data.
        orm_mode = True


# Additional properties stored in DB but not returned by API
class PhotoInDB(PhotoInDBBase):
    pass


# Additional properties to return via API
class Photo(PhotoInDBBase):
    pass