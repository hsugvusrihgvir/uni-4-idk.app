from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models import Idea, User
from app.db.queries.boards import BoardsQueries
from app.db.queries.ideas import IdeasQueries


class ModerationService:
    def __init__(self, db: Session) -> None:
        self.q_b = BoardsQueries(db)
        self.q_i = IdeasQueries(db)

    def pending(self, *, cur: User, board_id: UUID) -> list[Idea]:
        self._mod(cur=cur, board_id=board_id, msg="Only moderator can view moderation")
        return self.q_i.get_by_board_and_status(board_id=board_id, status="pending")

    def set_status(self, *, cur: User, idea_id: UUID, status: str) -> Idea:
        idea = self.q_i.get_by_id(idea_id=idea_id)
        if idea is None:
            raise ValueError("Idea not found")

        self._mod(cur=cur, board_id=idea.board_id, msg="Only moderator can change idea status")
        return self.q_i.update_status(idea=idea, status=status)

    def _mod(self, *, cur: User, board_id: UUID, msg: str) -> None:
        m = self.q_b.get_member(board_id=board_id, user_id=cur.id)
        if m is None:
            raise ValueError("Board not found")
        if m.role not in {"admin", "moderator"}:
            raise PermissionError(msg)
