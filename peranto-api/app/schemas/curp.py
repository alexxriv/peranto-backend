from typing import Optional, Sequence

from pydantic import BaseModel

class CurpBase(BaseModel):
    curp:str
    client_id: Optional[str]
    

class CurpCreate(CurpBase):
    curp: str

class CurpUpdate(CurpBase):
    ...

class CurpInDBBase(CurpBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True

class CurpInDB(CurpInDBBase):
    pass

class Curp(CurpInDBBase):
    pass

class CurpSearchResults(BaseModel):
    total: int
    results: Sequence[Curp]
