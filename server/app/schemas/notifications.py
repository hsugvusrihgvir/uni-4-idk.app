from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class NotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    text: str
    board_id: UUID | None
    created_at: datetime


class NotificationsListResponse(BaseModel):
    items: list[NotificationResponse]
