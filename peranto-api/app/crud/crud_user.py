from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email:str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()
    

    def create(self, db: Session, *, obj_in: UserCreate) -> User:

        create_data = obj_in.dict()
        create_data.pop("password")
        db_obj = User(**create_data) # We use ** to unpack the dictionary

        db_obj.hashed_password = get_password_hash(obj_in.password)

        db.add(db_obj)
        db.commit()

        return db_obj
    
    def create_with_kilt(self, db: Session, *, obj_in: UserCreate) -> User:

        create_data = obj_in.dict()
        create_data.pop("password")
        create_data["is_from_kilt"] = True
        db_obj = User(**create_data) # We use ** to unpack the dictionary
        db.add(db_obj)
        db.commit()

        return db_obj
    
    def update(
            self, db: Session, *, db_obj:User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User: # we overwrite the update method to avoid the error when we try to update the password
        if isinstance(obj_in, dict): # If obj_in is a dictionary, we do this to avoid the error
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True) # If obj_in is a UserUpdate object, we do this to avoid the error

        return super().update(db, db_obj=db_obj, obj_in=update_data)
    
    def is_superuser(self, user: User) -> bool:
        return user.is_superuser
    

user = CRUDUser(User)
