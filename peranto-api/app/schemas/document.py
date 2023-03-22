from typing import Optional, Sequence

from pydantic import BaseModel

class DocumentBase(BaseModel):
    document_id: Optional[str]
    client_id: Optional[str]
    document_type: Optional[str] = None
    classification: Optional[str] #The classification or purpose of this document. Valid values include: proof_of_identity, source_of_wealth ,source_of_funds, proof_of_address, company_filing, other
    #images: Optional[str] #The images associated with this document. This is a list of image IDs.
    created_at: bool = False
    updated_at: bool = False

class DocumentCreate(DocumentBase):
    document_id: str
    client_id: str
    document_type: str
    classification: str

class DocumentUpdate(DocumentBase):
    ...

class DocumentInDBBase(DocumentBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True

class DocumentInDB(DocumentInDBBase):
    pass

class Document(DocumentInDBBase):
    pass

class DocumentSearchResults(BaseModel):
    total: int
    results: Sequence[Document]
