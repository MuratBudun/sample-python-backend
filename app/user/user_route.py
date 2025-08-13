from fastapi import APIRouter, HTTPException

from app.user.user_schema import UserCreate, UserRead
from app.user.user_service import user_service
from common.database import DbDependency

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserRead, status_code=201)
async def create_user(user: UserCreate, db: DbDependency) -> UserRead:
    result = await user_service.create_user(db, user)
    if isinstance(result, str):
        raise HTTPException(status_code=400, detail=result)
    return result


@router.get("/{user_id}", response_model=UserRead)
async def read_user(user_id: str, db: DbDependency) -> UserRead:
    user = await user_service.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user