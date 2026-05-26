from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class VotingCreateRequest(BaseModel):
    type: Literal["like", "yes_no"]


class VotingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    board_id: UUID
    type: str
    created_at: datetime


class VotingsListResponse(BaseModel):
    items: list[VotingResponse]


class VoteCreateRequest(BaseModel):
    voting_id: UUID
    idea_id: UUID


class VoteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    voting_id: UUID
    idea_id: UUID
    created_at: datetime


class VotingResultItemResponse(BaseModel):
    idea_id: UUID
    title: str
    votes_count: int
    approval_percent: int
    user_voted: bool = False


class VotingResultsResponse(BaseModel):
    items: list[VotingResultItemResponse]
