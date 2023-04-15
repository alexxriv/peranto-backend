from typing import Optional, Sequence

from pydantic import BaseModel

class PassportBase(BaseModel):
    passport_type = str
    country_code = str
    passport_number = str
    last_names = str
    names = str
    country = str
    curp = str
    birth_date = str
    issue_date = str
    expiration_date = str

class PassportCreate(PassportBase):
    document_id: str
    client_id: str
    document_type: str
    classification: str

class PassportUpdate(PassportBase):
    ...

class PassportInDBBase(PassportBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True

class PassportInDB(PassportInDBBase):
    pass

class Passport(PassportInDBBase):
    pass

class PassportSearchResults(BaseModel):
    total: int
    results: Sequence[Passport]
