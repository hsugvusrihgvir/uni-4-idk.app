from uuid import UUID

from pydantic import BaseModel, constr


class TelegramLinkCodeResponse(BaseModel):
    code: str


class TelegramLinkRequest(BaseModel):
    code: constr(min_length=6, max_length=10)
    telegram_user_id: int


class TelegramChatBindRequest(BaseModel):
    board_id: UUID
    telegram_user_id: int
    telegram_chat_id: int
    chat_title: constr(max_length=255) | None = None


class TelegramChatResponse(BaseModel):
    board_id: UUID
    telegram_chat_id: int
    chat_title: str | None = None


class TelegramIdeaRequest(BaseModel):
    telegram_user_id: int
    telegram_chat_id: int
    text: constr(min_length=1, max_length=255)
