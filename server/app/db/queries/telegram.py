from uuid import UUID
from datetime import datetime, timedelta, timezone

from sqlalchemy import and_, select, update
from sqlalchemy.orm import Session, selectinload

from app.db.models import BoardTelegramChat, TgCode


class TelegramQueries:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_chat(self, *, telegram_chat_id: int) -> BoardTelegramChat | None:
        stmt = (
            select(BoardTelegramChat)
            .options(selectinload(BoardTelegramChat.board))
            .where(BoardTelegramChat.telegram_chat_id == telegram_chat_id)
            .limit(1)
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def bind_chat(self, *, board_id: UUID, telegram_chat_id: int, chat_title: str | None) -> BoardTelegramChat:
        chat = self.get_chat(telegram_chat_id=telegram_chat_id)

        if chat is None:
            chat = BoardTelegramChat(
                board_id=board_id,
                telegram_chat_id=telegram_chat_id,
                chat_title=chat_title,
            )
            self.db.add(chat)
        else:
            chat.board_id = board_id
            chat.chat_title = chat_title

        self.db.flush()
        return chat

    def create_link_code(self, *, user_id: UUID, code: str, ttl_minutes: int = 10) -> TgCode:
        now = datetime.now(timezone.utc)
        exp = now + timedelta(minutes=ttl_minutes)

        stmt = (
            update(TgCode)
            .where(and_(TgCode.user_id == user_id, TgCode.is_used.is_(False)))
            .values(is_used=True)
        )
        self.db.execute(stmt)

        row = TgCode(user_id=user_id, code=code, expires_at=exp, is_used=False)
        self.db.add(row)
        self.db.flush()
        return row

    def get_link_code(self, *, code: str) -> TgCode | None:
        now = datetime.now(timezone.utc)
        stmt = (
            select(TgCode)
            .options(selectinload(TgCode.user))
            .where(
                TgCode.code == code,
                TgCode.is_used.is_(False),
                TgCode.expires_at > now,
            )
            .order_by(TgCode.created_at.desc())
            .limit(1)
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def use_link_code(self, row: TgCode) -> None:
        row.is_used = True
        self.db.flush()
