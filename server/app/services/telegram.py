from uuid import UUID
import random

from sqlalchemy.orm import Session

from app.db.models import Idea, User
from app.db.queries.boards import BoardsQueries
from app.db.queries.telegram import TelegramQueries
from app.db.queries.users import UsersQueries
from app.services.ideas import IdeasService


class TelegramService:
    def __init__(self, db: Session) -> None:
        self.q_b = BoardsQueries(db)
        self.q_t = TelegramQueries(db)
        self.q_u = UsersQueries(db)
        self.ideas = IdeasService(db)

    def create_link_code(self, *, current_user: User) -> str:
        code = str(random.randint(100000, 999999))
        while self.q_t.get_link_code(code=code) is not None:
            code = str(random.randint(100000, 999999))

        self.q_t.create_link_code(user_id=current_user.id, code=code)
        return code

    def link_user(self, *, code: str, telegram_user_id: int) -> User:
        row = self.q_t.get_link_code(code=code)
        if row is None:
            raise ValueError("Invalid or expired code")

        user = row.user

        taken = self.q_u.get_by_tg_id(telegram_user_id)
        if taken is not None and taken.id != user.id:
            raise ValueError("Telegram account already linked")

        self.q_t.use_link_code(row)
        return self.q_u.set_tg_id(user=user, tg_id=telegram_user_id)

    def bind_chat(
        self,
        *,
        board_id: UUID,
        telegram_user_id: int,
        telegram_chat_id: int,
        chat_title: str | None,
    ):
        user = self.q_u.get_by_tg_id(telegram_user_id)
        if user is None:
            raise ValueError("Telegram account not linked")

        member = self.q_b.get_member(board_id=board_id, user_id=user.id)
        if member is None:
            raise ValueError("Board not found")
        if member.role != "admin":
            raise PermissionError("Only board admin can bind telegram chat")

        return self.q_t.bind_chat(board_id=board_id, telegram_chat_id=telegram_chat_id, chat_title=chat_title)

    def create_idea_from_chat(self, *, telegram_user_id: int, telegram_chat_id: int, text: str) -> Idea:
        user = self.q_u.get_by_tg_id(telegram_user_id)
        if user is None:
            raise ValueError("Telegram account not linked")

        chat = self.q_t.get_chat(telegram_chat_id=telegram_chat_id)
        if chat is None:
            raise ValueError("Telegram chat is not linked to board")

        return self.ideas.create(
            current_user=user,
            board_id=chat.board_id,
            title=text.strip(),
            description=None,
            is_anonymous=False,
        )
