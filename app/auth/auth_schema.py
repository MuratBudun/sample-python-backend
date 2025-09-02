from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: Optional[str] = None

class TokenUser(BaseModel):
    id: str 
    full_name: str | None = None
    username: str | None = None
    email: str | None = None  
    exp: datetime | None = None
    groups: list[str] | None = None
    reset_password: bool | None = None
