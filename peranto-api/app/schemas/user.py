from typing import Optional

from pydantic import BaseModel, EmailStr



class UserBase(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr] = None
    is_superuser: Optional[bool] = False

# Properties to recieve via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str


# Properties to recieve via API on update
class UserUpdate(UserBase):
    ...


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional preoperties stored in DB but not returned by APi
class UserInDB(UserInDBBase):
    hashed_password: str


# Additional properties to return via API
class User(UserInDBBase):
    ...

