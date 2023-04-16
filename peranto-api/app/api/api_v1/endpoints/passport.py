import logging

from typing import Any, Optional

from fastapi import APIRouter, Query, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.schemas.passport import Passport, PassportCreate, PassportUpdate, PassportSearchResults
from app.models.user import User

router = APIRouter()
logger = logging.getLogger(__name__)



@router.get("/{passport_id}", status_code=200, response_model=Passport)
def fetch_passport(
    *,
    db: Session = Depends(deps.get_db),
    passport_id: int,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve a passport owned by the current user.
    """

    passport = crud.passport.get(db=db, id=passport_id)
    if not passport:
        raise HTTPException(status_code=404, detail=f"passport with id {passport_id} not found")
    if passport.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return passport


@router.get("/my-passports/", status_code=200, response_model=PassportSearchResults)
def fetch_my_passports(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> dict:
    """
    Retrieve all passports for the current user.
    """
    passports = current_user.passports
    if not passports:
        return {"results": []}
    
    return {"results": list(passports)}


@router.post("/", status_code=201, response_model=Any) # TODO response_model=Passport
def create_passport(
    *,
    db: Session = Depends(deps.get_db),
    passport_in: PassportCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Create a new passport for the current user, owner id must be the current user.
    """
    if passport_in.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    passport = crud.passport.create(db=db, obj_in=passport_in)
    logger.debug(f"passport created with id {passport.id}")
    return passport
    