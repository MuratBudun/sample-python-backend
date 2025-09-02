from tokenize import Token
from fastapi import APIRouter, HTTPException

from app.auth.auth_schema import TokenUser
from app.auth.auth_service import DpCurrentUser
from app.user.user_model import User, UserStatus
from app.user.user_schema import UserBase, UserCreate, UserRead
from app.user.user_service import user_service
from common.database import DbDependency

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserRead, status_code=201)
async def create_user(user: UserCreate, db: DbDependency) -> UserRead:
    result = await user_service.create_user(db, user)
    if isinstance(result, str):
        raise HTTPException(status_code=400, detail=result)
    return result

@router.get("/me", response_model=UserRead)
async def read_current_user(user: DpCurrentUser, db: DbDependency) -> UserRead:
    db_user = await user_service.get_user_by_id(db, user.id)
    if db_user is None or db_user.status == UserStatus.DISABLED:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/{user_id}", response_model=UserRead)
async def read_user(user_id: str, db: DbDependency) -> UserRead:
    user = await user_service.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user