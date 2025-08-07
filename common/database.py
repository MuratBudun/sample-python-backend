from settings import settings
from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base

Base = declarative_base(metadata=MetaData(schema=settings.DATABASE_SCHEMA))
