from sqlalchemy.orm import Session

from app.db.queries.boards import BoardsQueries
from app.db.models import Board, BoardMember, User


class BoardsService:
    def __init__(self, db: Session) -> None:
        self.q_b = BoardsQueries(db)

    def create(
        self,
        *,
        current_user: User,
        title: str,
        description: str | None,
        moderation: bool,
        anon_ideas: bool,
    ) -> Board:
        board = self.q_b.create(title=title, description=description, moderation=moderation, anon_ideas=anon_ideas)

        self.q_b.add_member(board_id=board.id, user_id=current_user.id, role="admin")

        return board

    def get_my_boards(self, *, current_user: User) -> list[BoardMember]:
        return self.q_b.get_my_boards(user_id=current_user.id)

    def get_board(self, *, current_user: User, board_id) -> BoardMember:
        member = self.q_b.get_by_id_for_user(board_id=board_id, user_id=current_user.id)

        if member is None:
            raise ValueError("Board not found")

        return member
