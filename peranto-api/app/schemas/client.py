from typing import Optional

from pydantic import BaseModel, EmailStr


class ClientBase(BaseModel):
    first_name: Optional[str]
    surname: Optional[str]
    email: Optional[EmailStr] = None
    is_superuser: bool = False


# Properties to receive via API on creation
class ClientCreate(ClientBase):
    email: EmailStr
    password: str


# Properties to receive via API on update
class ClientUpdate(ClientBase):
    ...


class ClientInDBBase(ClientBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties stored in DB but not returned by API
class ClientInDB(ClientInDBBase):
    hashed_password: str


# Additional properties to return via API
class Client(ClientInDBBase):
    ...