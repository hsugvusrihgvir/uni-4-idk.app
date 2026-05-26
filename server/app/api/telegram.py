import os

from fastapi import APIRouter, Depends, Header, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.models import User
from app.db.session import get_db
from app.schemas.ideas import IdeaResponse
from app.schemas.telegram import (
    TelegramChatBindRequest,
    TelegramChatResponse,
    TelegramIdeaRequest,
    TelegramLinkCodeResponse,
    TelegramLinkRequest,
)
from app.services.idea_ws import ideas_ws
from app.services.telegram import TelegramService

router = APIRouter(prefix="/api/v1/telegram", tags=["Telegram"])


def check_bot_secret(x_bot_secret: str | None = Header(default=None)) -> None:
    secret = os.getenv("TELEGRAM_BOT_SECRET")
    if not secret or x_bot_secret != secret:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid bot secret")


@router.post("/link-code", response_model=TelegramLinkCodeResponse)
def create_link_code(cur: User = Depends(get_current_user), db: Session = Depends(get_db)):
    code = TelegramService(db).create_link_code(current_user=cur)
    return TelegramLinkCodeResponse(code=code)


@router.post("/users/link", dependencies=[Depends(check_bot_secret)])
def link_user(body: TelegramLinkRequest, db: Session = Depends(get_db)):
    try:
        TelegramService(db).link_user(code=body.code, telegram_user_id=body.telegram_user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return {"message": "Telegram account linked"}


@router.post("/chats/bind", response_model=TelegramChatResponse, dependencies=[Depends(check_bot_secret)])
def bind_chat(body: TelegramChatBindRequest, db: Session = Depends(get_db)):
    try:
        chat = TelegramService(db).bind_chat(
            board_id=body.board_id,
            telegram_user_id=body.telegram_user_id,
            telegram_chat_id=body.telegram_chat_id,
            chat_title=body.chat_title,
        )
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return TelegramChatResponse(
        board_id=chat.board_id,
        telegram_chat_id=chat.telegram_chat_id,
        chat_title=chat.chat_title,
    )


@router.post("/ideas", response_model=IdeaResponse, dependencies=[Depends(check_bot_secret)])
async def create_idea(body: TelegramIdeaRequest, db: Session = Depends(get_db)):
    try:
        idea = TelegramService(db).create_idea_from_chat(
            telegram_user_id=body.telegram_user_id,
            telegram_chat_id=body.telegram_chat_id,
            text=body.text,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    data = IdeaResponse.model_validate(idea)
    await ideas_ws.broadcast(
        board_id=idea.board_id,
        data={
            "type": "idea_created",
            "idea": jsonable_encoder(data),
        },
    )
    return data
