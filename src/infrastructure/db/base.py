from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from settings import settings

Base = DeclarativeBase
AsyncBase = type("AsyncBase", (AsyncAttrs, Base), {})

engine = create_async_engine(url=settings.POSTGRES_DSN.unicode_string())
session_factory = async_sessionmaker(bind=engine, expire_on_commit=True)
