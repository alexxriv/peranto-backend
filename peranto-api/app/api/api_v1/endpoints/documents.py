import asyncio
from typing import Any, Optional

import httpx
from fastapi import APIRouter
from app.schemas.document import Document, DocumentCreate, DocumentUpdate, DocumentSearchResults

router = APIRouter()

@router.get("/")
async def get_documents():
    # Returns a list of documents, json for the moment
    return {"total": 0, "results": [
        {"document_id": "123", "client_id": "123", "document_type": "passport", "classification": "proof_of_identity", "created_at": "2021-01-01", "updated_at": "2021-01-01"},
        {"document_id": "456", "client_id": "456", "document_type": "passport", "classification": "proof_of_identity", "created_at": "2021-01-01", "updated_at": "2021-01-01"},
        {"document_id": "789", "client_id": "789", "document_type": "passport", "classification": "proof_of_identity", "created_at": "2021-01-01", "updated_at": "2021-01-01"}
    ]}