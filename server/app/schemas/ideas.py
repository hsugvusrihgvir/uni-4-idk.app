from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, constr


class IdeaCreateRequest(BaseModel):
    title: constr(max_length=255)
    description: str | None = None
    id_board: UUID
    is_anonymous: bool = False


class IdeaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    id_board: UUID
    title: str
    description: str | None
    status: str
    is_anonymous: bool
    created_at: datetime


class IdeaItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str | None
    status: str


class IdeasListResponse(BaseModel):
    items: list[IdeaResponse]
