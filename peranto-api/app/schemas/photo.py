from typing import Optional

from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Sequence


class PhotoBase(BaseModel):
    label: str
    source: Optional[str]
    url: HttpUrl



# Properties to receive via API on creation
class PhotoCreate(PhotoBase):
    label: str
    source: str
    url: HttpUrl
    owner_id: int


# Properties to receive via API on update
class PhotoUpdate(PhotoBase):
    label: str


class PhotoInDBBase(PhotoBase):
    id: int
    owner_id: int

    class Config: # This orm_mode is required to allow Pydantic to read the data even if it is not a dict, but an ORM model. Without it if you return a SQLAlchemy model from your path operation it wouldnt include the relationship data.
        orm_mode = True


# Additional properties stored in DB but not returned by API
class PhotoInDB(PhotoInDBBase):
    pass


# Additional properties to return via API
class Photo(PhotoInDBBase):
    pass


class PhotoSearchResults(BaseModel):
    results: Sequence[Photo]