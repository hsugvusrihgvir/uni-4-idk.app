from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models import User, Voting
from app.db.queries.boards import BoardsQueries
from app.db.queries.votings import VotingsQueries
from app.services.votings import ALLOWED_TYPES


class VotingAdminService:
    def __init__(self, db: Session) -> None:
        self.q_b = BoardsQueries(db)
        self.q_v = VotingsQueries(db)

    def create(self, *, cur: User, board_id: UUID, type: str) -> Voting:
        self._admin(cur=cur, board_id=board_id, msg="Only admin can create voting")

        if type not in ALLOWED_TYPES:
            raise ValueError("Invalid voting type")

        return self.q_v.create(board_id=board_id, type=type)

    def delete(self, *, cur: User, voting_id: UUID) -> None:
        voting = self.q_v.get_by_id(voting_id=voting_id)
        if voting is None:
            raise ValueError("Voting not found")

        self._admin(cur=cur, board_id=voting.board_id, msg="Only admin can delete voting")
        self.q_v.delete(voting)

    def _admin(self, *, cur: User, board_id: UUID, msg: str) -> None:
        m = self.q_b.get_member(board_id=board_id, user_id=cur.id)
        if m is None:
            raise ValueError("Board not found")
        if m.role != "admin":
            raise PermissionError(msg)
