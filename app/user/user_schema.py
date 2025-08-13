from typing import Optional
from pydantic import BaseModel, Field
from app.user.user_model import UserStatus

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    full_name: str = Field(..., max_length=150)
    email: str = Field(..., max_length=100)
    status: UserStatus

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    force_password_change: Optional[bool] = False
    use_ldap: Optional[bool] = False

class UserUpdate(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    full_name: str = Field(..., max_length=150)
    email: str = Field(..., max_length=100)
    status: UserStatus
    force_password_change: Optional[bool]
    use_ldap: Optional[bool]

class UserRead(UserBase):
    id: str
    force_password_change: Optional[bool]
    use_ldap: Optional[bool]

    class Config:
        from_attributes = True