from typing import Any
import logging 

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session

from app import crud
from app import schemas
from app.api import deps
from app.core.auth import (
    authenticate,
    create_access_token
)
from app.models.user import User

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/login")
def login(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Get the JWT for a user with data from OAuth2 request form body
    """
    logger.info("User logging in")
    user = authenticate(email=form_data.username, password=form_data.password, db=db)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    #access_token = create_access_token(data={"sub": user.email})
    #return {"access_token": access_token, "token_type": "bearer"}

    return {
        "access_token": create_access_token(sub=user.email),
        "token_type": "bearer",
    }


@router.post("/signup", response_model=schemas.User, status_code=201)
def create_user_signup(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
) -> Any:
    logger.info("Creating user")
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = crud.user.create(db, obj_in=user_in)
    #access_token = create_access_token(data={"sub": user.email})
    #return {"access_token": access_token, "token_type": "bearer"}
    return user


@router.get("/me", response_model=schemas.User)
def read_users_me(
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


