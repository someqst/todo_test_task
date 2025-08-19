from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from core.config import settings


engine = create_async_engine(settings.POSTGRES_URL)
LocalSession = async_sessionmaker(bind=engine)
