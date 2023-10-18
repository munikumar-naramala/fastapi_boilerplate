from fastapi import APIRouter

from app.api.endpoints import user_management

api_router = APIRouter()
api_router.include_router(user_management.router, prefix="/v1", tags=["User Management"])
