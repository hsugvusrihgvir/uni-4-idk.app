from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, constr

from app.schemas.ideas import IdeaItemResponse


# POST /api/v1/boards
class BoardCreateRequest(BaseModel):
    title: constr(max_length=255)
    description: str | None = None
    moderation: bool = True
    anon_ideas: bool = True


class BoardCreateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str | None
    moderation: bool
    anon_ideas: bool


# GET /api/v1/boards
class BoardItemResponse(BaseModel):
    id: UUID
    title: str
    description: str | None
    role: str
    ideas_count: int = 0
    members_count: int = 0


class BoardsListResponse(BaseModel):
    items: list[BoardItemResponse]


# GET /api/v1/boards/{board_id}
class BoardDetailResponse(BaseModel):
    id: UUID
    title: str
    description: str | None
    role: str
    anon_ideas: bool
    moderation: bool
    created_at: datetime
    ideas: list[IdeaItemResponse]


class BoardUpdateRequest(BaseModel):
    title: constr(max_length=255) | None = None
    description: str | None = None
    moderation: bool | None = None
    anon_ideas: bool | None = None


class BoardMemberCreateRequest(BaseModel):
    username: constr(max_length=50, min_length=3)
    role: Literal["admin", "moderator", "member"] = "member"


class BoardMemberRoleRequest(BaseModel):
    role: Literal["admin", "moderator", "member"]


class BoardMemberResponse(BaseModel):
    id: UUID
    username: str
    name: str | None
    photo_url: str | None
    role: str


class BoardMembersListResponse(BaseModel):
    items: list[BoardMemberResponse]
