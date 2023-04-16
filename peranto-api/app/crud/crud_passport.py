from app.crud.base import CRUDBase
from app.models.passport import Passport
from app.schemas.passport import PassportCreate, PassportUpdate


class CRUDPassport(CRUDBase[Passport, PassportCreate, PassportUpdate]):
    ...


passport = CRUDPassport(Passport)
