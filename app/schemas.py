from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class StartBody(BaseModel):
    region: str


class StartResponse(BaseModel):
    uuid: UUID


class EndBody(StartResponse):
    intermediate: Optional[bool] = False
    pass


class EndResponse(BaseModel):
    energy: float
    time: float
    power: Optional[list]
    ts: Optional[list]
