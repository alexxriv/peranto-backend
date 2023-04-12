#A necessity for a smooth Identity Check user experience.
#Live photos are images (i.e. selfies) of the client's face. Typically, along with an ID document, they are used to perform .
#Upon creating a Live Photo, the following inspections are conducted:
#Faces Analysis: checks if a face is detected and that the number of faces does not exceed 1.
#Facial Obstructions: checks if facial features are covered or not visible.
#Facial Orientation: checks if a face is at an optimal position.
#Liveness Check: checks if a photo is genuine and is not a spoofed photo of an image or photo-of-a-photo.
#The live photos API allows you to upload, retrieve, download, and delete live photos. You can retrieve a specific live photo as well as a list of all your client's live photos.

import asyncio
from typing import Any, Optional

from fastapi import APIRouter, Query, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.schemas.photo import Photo, PhotoCreate, PhotoUpdate, PhotoSearchResults

router = APIRouter()

@router.get("/{photo_id}", status_code=200, response_model=Photo)
def fetch_photo(
    *,
    db: Session = Depends(deps.get_db),
    photo_id: int,
    current_user: Any = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve a photo.
    """
    photo = crud.photo.get(db=db, id=photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail=f"photo with id {photo_id} not found")
    return photo

@router.get("/search/", status_code=200, response_model=PhotoSearchResults)
def search_photos(
    *,
    keyword: str = Query(None, min_length=3, example="chicken"),
    max_results: Optional[int] = 10,
    db: Session = Depends(deps.get_db),
) -> dict:
    """
    Search for photos based on label keyword
    """
    photos = crud.photo.get_multi(db=db, limit=max_results)
    results = filter(lambda photo: keyword.lower() in photo.label.lower(), photos)

    return {"results": list(results)}


@router.post("/", status_code=201, response_model=Photo)
def create_photo(
    *, photo_in: PhotoCreate, db: Session = Depends(deps.get_db)
) -> dict:
    """
    Create a new photo in the database.
    """
    photo = crud.photo.create(db=db, obj_in=photo_in)

    return photo