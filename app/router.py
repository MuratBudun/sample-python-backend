from fastapi import APIRouter
from app.user.user_route import router as user_router

router = APIRouter(prefix="/api")

router.include_router(user_router)