from typing import Any, Optional

from fastapi import APIRouter, Query, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.schemas.curp import Curp, CurpCreate, CurpUpdate, CurpSearchResults
from app.models.user import User

router = APIRouter()

@router.get("/{curp_id}", status_code=200, response_model=Curp)
def fetch_curp(
    *,
    db: Session = Depends(deps.get_db),
    curp_id: int,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve a curp owned by the current user.
    """
    curp = crud.curp.get(db=db, id=curp_id)
    if not curp:
        raise HTTPException(status_code=404, detail=f"curp with id {curp_id} not found")
    if curp.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return curp


@router.get("/my-curp", status_code=200, response_model=Curp)
def fetch_my_curp(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> dict:
    """
    Retrieve curp for the current user.
    """
    curp = current_user.curp
    print(curp)
    if not curp:
        return {"curp": None}
    
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