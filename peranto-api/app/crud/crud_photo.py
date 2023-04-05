from app.crud.base import CRUDBase

from app.models.photo import Photo

from app.schemas.photo import PhotoCreate, PhotoUpdate


class CRUDPhoto(CRUDBase[Photo, PhotoCreate, PhotoUpdate]):
    ...


photo = CRUDPhoto(Photo)