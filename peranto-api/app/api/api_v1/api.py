from fastapi import APIRouter

from app.api.api_v1.endpoints import photos, clients, documents

api_router = APIRouter()

#api_router.include_router(clients.router, prefix="/users", tags=["users"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])