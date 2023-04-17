import logging
from sqlite3 import IntegrityError

from typing import Any, Optional

from fastapi import APIRouter, Query, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.schemas.passport import PassportCreate, PassportUpdate, Passport
from app.models.user import User

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/", status_code=200, response_model=Passport)
def fetch_my_passport(
    *,
    current_user: User = Depends(deps.get_current_user),
) -> dict:
    """
    Retrieve passport for the current user.
    """
    passport = current_user.passport
    if not passport:
        raise HTTPException(status_code=404, detail="No passport found")
    return passport


@router.post("/", status_code=201, response_model=Passport) 
def create_passport(
    *,
    db: Session = Depends(deps.get_db),
    passport_in: PassportCreate,
    current_user: User = Depends(deps.get_current_user),
) -> dict:
    """
    Create a new passport for the current user, owner id must be the current user.
    """
    if passport_in.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    passport = current_user.passport
    if passport:
        raise HTTPException(status_code=400, detail="Passport already exists")
    passport = crud.passport.create(db=db, obj_in=passport_in)
    return passport


@router.put("/{passport_id}", status_code=200, response_model=Passport)
def update_passport(
    *,
    db: Session = Depends(deps.get_db),
    passport_id: int,
    passport_in: PassportUpdate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Update a passport owned by the current user.
    """
    passport = crud.passport.get(db=db, id=passport_id)
    if not passport:
        raise HTTPException(status_code=404, detail=f"passport with id {passport_id} not found")
    if passport.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    passport = crud.passport.update(db=db, db_obj=passport, obj_in=passport_in)
    return passport

@router.delete("/", status_code=200)
def delete_passport(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete a passport owned by the current user.
    We get all  owned by current user and delte them
    """

    passport = current_user.passport
    if not passport:
        raise HTTPException(status_code=404, detail="No passport found")
    passport = crud.passport.remove(db=db, id=passport.id)
    return {"message": "Passport deleted"}

    