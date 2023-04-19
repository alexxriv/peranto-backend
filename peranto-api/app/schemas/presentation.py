from typing import Optional, Sequence

from pydantic import BaseModel

class PresentationBase(BaseModel):
    presentation:str
    

class PresentationCreate(PresentationBase):
    presentation: str


class Presentation(PresentationBase):
    pass

