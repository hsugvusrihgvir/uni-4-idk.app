from uuid import UUID

from sqlalchemy.orm import Session

from app.db.queries.boards import BoardsQueries
from app.db.queries.ideas import IdeasQueries
from app.db.models import Idea, User


class IdeasService:
    def __init__(self, db: Session) -> None:
        self.q_boards = BoardsQueries(db)
        self.q_ideas = IdeasQueries(db)

    def create(
        self,
        *,
        current_user: User,
        board_id: UUID,
        title: str,
        description: str | None,
        is_anonymous: bool,
    ) -> Idea:
        member = self.q_boards.get_by_id_for_user(board_id=board_id, user_id=current_user.id)

        if member is None:
            raise ValueError("Board not found")

        if is_anonymous and not member.board.anon_ideas:
            raise ValueError("Anonymous ideas are disabled")

        status = "pending" if member.board.moderation else "approved"

        return self.q_ideas.create(
            board_id=board_id,
            user_id=current_user.id,
            title=title,
            description=description,
            status=status,
            is_anonymous=is_anonymous,
        )

    def get_by_board(
        self,
        *,
        current_user: User,
        board_id: UUID,
    ) -> list[Idea]:
        member = self.q_boards.get_member(board_id=board_id, user_id=current_user.id)

        if member is None:
            raise ValueError("Board not found")

        return self.q_ideas.get_by_board(board_id=board_id)

    def delete(self, *, current_user: User, idea_id: UUID) -> None:
        idea = self.q_ideas.get_by_id(idea_id=idea_id)

        if idea is None:
            raise ValueError("Idea not found")

        if idea.id_user != current_user.id:
            raise PermissionError("Only author can delete idea")

        self.q_ideas.delete(idea)
