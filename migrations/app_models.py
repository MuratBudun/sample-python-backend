from common.database import Base
from app.user.user_model import User

app_db_metadata = Base.metadata

__all__ = [
    "app_db_metadata",
    "User"
]