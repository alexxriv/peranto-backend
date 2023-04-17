import logging
from typing import Any, Optional

from fastapi import APIRouter, Query, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.schemas.curp import Curp, CurpCreate, CurpUpdate
from app.models.user import User

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/", status_code=200, response_model=Curp)
def fetch_my_curp(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> dict:
    """
    Retrieve curp for the current user.
    """
    logger.debug("fetch_my_curp")
    curp = current_user.curp
    if not curp:
        raise HTTPException(status_code=404, detail="No curp found")
    
    return curp


@router.post("/", status_code=201, response_model=Curp)
def create_curp(
    *, 
    curp_in: CurpCreate, 
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> dict:
    """
    Create a new curp in the database.
    """

    if curp_in.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="You can only create curp for yourself")
    if current_user.curp:
        raise HTTPException(status_code=400, detail="You already have a curp")
    curp = crud.curp.create(db=db, obj_in=curp_in)

    return curp


@router.put("/", status_code=200, response_model=Curp)
def update_curp(
    *,
    db: Session = Depends(deps.get_db),
    curp_in: CurpUpdate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Update a curp owned by the current user.
    """
    curp = current_user.curp
    if not curp:
        raise HTTPException(status_code=404, detail=f"user {current_user.id} has no curp")
    curp = crud.curp.update(db=db, db_obj=curp, obj_in=curp_in)
    return curp

@router.delete("/", status_code=200,)
def delete_curp(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete a curp owned by the current user.
    """
    curp = current_user.curp
    if not curp:
        raise HTTPException(status_code=404, detail=f"user {current_user.id} has no curp")
    curp = crud.curp.remove(db=db, id=curp.id)
    return curp