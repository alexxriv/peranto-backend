from typing import Optional, Sequence

from pydantic import BaseModel

class PassportBase(BaseModel):
    document_id: Optional[str]
    client_id: Optional[str]
    document_type: Optional[str] = None
    classification: Optional[str] #The classification or purpose of this document. Valid values include: proof_of_identity, source_of_wealth ,source_of_funds, proof_of_address, company_filing, other
    #images: Optional[str] #The images associated with this document. This is a list of image IDs.
    created_at: bool = False
    updated_at: bool = False

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
