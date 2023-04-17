from fastapi import APIRouter

from app.api.api_v1.endpoints import photo, auth, passport, curp
api_router = APIRouter()

#api_router.include_router(clients.router, prefix="/users", tags=["users"])
#api_router.include_router(documents.router, prefix="/documents", tags=["documents"])

api_router.include_router(photo.router, prefix="/photo", tags=["photo"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(passport.router, prefix="/passport", tags=["passport"])
api_router.include_router(curp.router, prefix="/curp", tags=["curp"])
