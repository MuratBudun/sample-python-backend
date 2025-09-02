from typing import Optional, Union
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common.security import get_password_hash, verify_password
from app.user.user_schema import UserCreate, UserRead
from app.user.user_model import User

class UserService:
    async def create_user(self, db: AsyncSession, user_data: UserCreate) -> Union[User, str]:
        db_user = await self.get_user_by_username(db, user_data.username)
        if db_user:
            return "Username already registered"

        db_user_email = await self.get_user_by_email(db, user_data.email)
        if db_user_email:
            return "Email already registered"

        user_data_dict = user_data.model_dump(exclude={"password"})
        db_user = User(**user_data_dict)

        # Set hashed password separately
        password_hash = get_password_hash(user_data.password)
        setattr(db_user, "hashed_password", password_hash)

        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    async def validate_password(self, db: AsyncSession, username_or_email: str, password: str) -> Optional[UserRead]:
        user = await self.get_user_by_username(db, username_or_email)
        if not user:
            user = await self.get_user_by_email(db, username_or_email)

        if user is None:
            return None

        if not user or not verify_password(password, user.hashed_password):
            return None
        
        return user

    #region get user ...
    async def get_user_by_id(self, db: AsyncSession, user_id: str) -> Optional[User]:
        query = select(User).where(User.id == user_id)
        result = await db.execute(query)

        return result.scalar_one_or_none()        

    async def get_user_by_username(self, db: AsyncSession, username: str) -> Optional[User]:
        query = select(User).where(User.username == username)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_user_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        query = select(User).where(User.email == email)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    #endregion

user_service = UserService()