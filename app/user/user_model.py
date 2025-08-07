from enum import Enum
import uuid
from sqlalchemy import Column, String, Unicode, DateTime, Boolean, func, Enum as SqlEnum
from common.database import Base

class UserStatus(Enum):
    ACTIVE = "active"
    DISABLED = "disabled"

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    username = Column(Unicode(100), index=True)
    full_name = Column(Unicode(150))
    title = Column(Unicode(150))
    email = Column(Unicode(200), index=True)
    hashed_password = Column(String)
    status = Column(SqlEnum(UserStatus), default=UserStatus.ACTIVE)
    force_password_change = Column(Boolean)
    use_ldap = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())