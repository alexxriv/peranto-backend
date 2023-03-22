from typing import Optional

from pydantic import BaseModel, EmailStr


class PhotoBase(BaseModel):
    photo_id: Optional[str]
    client_id: Optional[str]
    dowload_link: Optional[EmailStr] = None
    size: bool = False
    created_at: bool = False
    updated_at: bool = False



# Properties to receive via API on creation
class PhootCreate(PhotoBase):
    photo_id: EmailStr


# Properties to receive via API on update
class PhotoUpdate(PhotoBase):
    ...


class PhotoInDBBase(PhotoBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties stored in DB but not returned by API
class PhotoInDB(PhotoInDBBase):
    content_type: str


# Additional properties to return via API
class Photo(PhotoInDBBase):
    ...