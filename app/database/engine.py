from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URI = "sqlite+aiosqlite:///./products.db"

engine = create_async_engine(SQLALCHEMY_DATABASE_URI, echo=True)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False, autocommit=False
)


Base = declarative_base()
