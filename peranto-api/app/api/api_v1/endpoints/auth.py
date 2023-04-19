import json
from typing import Any
import logging 
import asyncio
import httpx
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
from app.clients.kilt import KiltClient


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

    response = {
        "access_token": create_access_token(sub=user.email),
        "token_type": "bearer",
    }

    logger.info(response)
    return response


@router.post("/kilt-login")
async def login(
    *,
    kilt_client: KiltClient = Depends(deps.get_kilt_client),
    presentation: schemas.PresentationCreate,
) -> Any:
    """
    Get the JWT for a user with data from OAuth2 request form body
    """
    logger.debug(presentation)
    return ""
    logger.debug(json.loads(presentation))
    return ""
    logger.info("User logging in")
    async with httpx.AsyncClient(timeout=90) as client:
        response = await client.post(
            kilt_client.base_url + "present",
            json={"presentation": presentation},
        )
        response.raise_for_status()
        logger.info(response)
    logger.debug(response.json())
    response = {
        "access_token": create_access_token(sub=json.loads(presentation).claim.contents.email),
        "token_type": "bearer",
    }

    logger.info(response)
    return response


@router.post("/kilt-signup")
async def login(
    *,
    db: Session = Depends(deps.get_db),
    kilt_client: KiltClient = Depends(deps.get_kilt_client),
    user_in: schemas.UserCreate,
    light_did_uri: str,

) -> Any:
    """
    Create a user with data from KILT
    """
    logger.info("User signing up")
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        logger.info("user already exists")
        raise HTTPException(status_code=400, detail="Email already registered")
    
    #Post request with json body {"email": email, "lightDidUri": light_did_uri}
    async with httpx.AsyncClient(timeout=90) as client:
        response = await client.post(
            kilt_client.base_url + "register",
            json={"email": user_in.email, "lightDidUri": light_did_uri},
        )
        response.raise_for_status()
        logger.info(response)
    logger.debug(response.json())
    crud.user.create(db, obj_in=user_in)
    return response.json()
    



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


