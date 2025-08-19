from pytz import timezone
from uuid import UUID, uuid4
from datetime import datetime
from api.schema.todo import StatusEnum
from sqlalchemy import Text, DateTime, Uuid, String
from sqlalchemy.orm import mapped_column, DeclarativeBase, Mapped


class Base(DeclarativeBase):
    pass


class Tasks(Base):
    __tablename__ = "tasks"
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, unique=True, default=uuid4, index=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[StatusEnum] = mapped_column(String(11), default=StatusEnum.TODO)
    creation_time: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(timezone("Europe/Moscow")).replace(tzinfo=None)
    )
