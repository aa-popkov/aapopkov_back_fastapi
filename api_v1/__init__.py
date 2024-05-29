from fastapi import APIRouter

from .routers.auth import router as auth_router
from .routers.user import router as user_router
from .routers.client import router as client_router

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(auth_router)
api_v1_router.include_router(user_router)
api_v1_router.include_router(client_router)

__all__ = ["api_v1_router"]
