from typing import Optional, Sequence

from pydantic import BaseModel

class CurpBase(BaseModel):
    curp:str
    

class CurpCreate(CurpBase):
    curp: str
    owner_id: int

class CurpUpdate(CurpBase):
    curp:str

class CurpInDBBase(CurpBase):
    id: Optional[int] = None
    owner_id: int

    class Config:
        orm_mode = True

class CurpInDB(CurpInDBBase):
    pass

class Curp(CurpInDBBase):
    pass

class CurpSearchResults(BaseModel):
    results: Sequence[Curp]
