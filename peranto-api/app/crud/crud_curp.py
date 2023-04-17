from app.crud.base import CRUDBase

from app.models.curp import Curp

from app.schemas.curp import CurpCreate, CurpUpdate


class CRUDCurp(CRUDBase[Curp, CurpCreate, CurpUpdate]):
    ...


curp = CRUDCurp(Curp)