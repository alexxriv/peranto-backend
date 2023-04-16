from typing import Any, Optional

from fastapi import APIRouter, Query, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.schemas.passport import Passport, PassportCreate, PassportUpdate, PassportSearchResults


router = APIRouter()

