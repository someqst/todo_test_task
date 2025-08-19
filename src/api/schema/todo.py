from pydantic import BaseModel, ConfigDict
from datetime import datetime
from enum import StrEnum
from uuid import UUID
from typing import Optional


class ToDoCreate(BaseModel):
    title: str
    description: str


class ToDoFromDB(BaseModel):
    id: UUID
    title: str
    description: str
    status: str
    creation_time: datetime

    model_config = ConfigDict(from_attributes=True)


class StatusEnum(StrEnum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class BaseResponse(BaseModel):
    status: str
    data: list | dict | str
