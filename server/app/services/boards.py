from uuid import UUID

from sqlalchemy.orm import Session

from app.db.queries.boards import BoardsQueries
from app.db.models import Board, BoardMember, User


class BoardsService:
    def __init__(self, db: Session) -> None:
        self.q_boards = BoardsQueries(db)

    def create(
        self,
        *,
        current_user: User,
        title: str,
        description: str | None,
        moderation: bool,
        anon_ideas: bool,
    ) -> Board:
        board = self.q_boards.create(title=title, description=description, moderation=moderation, anon_ideas=anon_ideas)

        self.q_boards.add_member(board_id=board.id, user_id=current_user.id, role="admin")

        return board

    def get_my_boards(self, *, current_user: User) -> list[BoardMember]:
        return self.q_boards.get_my_boards(user_id=current_user.id)

    def get_board(
        self,
        *,
        current_user: User,
        board_id: UUID,
    ) -> BoardMember:
        member = self.q_boards.get_by_id_for_user(board_id=board_id, user_id=current_user.id)

        if member is None:
            raise ValueError("Board not found")

        return member

    def delete(self, *, current_user: User, board_id: UUID) -> None:
        member = self.q_boards.get_member(board_id=board_id, user_id=current_user.id)

        if member is None:
            raise ValueError("Board not found")

        if member.role != "admin":
            raise PermissionError("Only admin can delete board")

        self.q_boards.delete(member.board)
