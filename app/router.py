from fastapi import APIRouter
from app.user.user_route import router as user_router
from app.auth.auth_route import router as auth_router

router = APIRouter(prefix="/api")

router.include_router(user_router)
router.include_router(auth_router)