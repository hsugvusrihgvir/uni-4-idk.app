from sqlalchemy.orm import Session

from app.db.models import Board, BoardMember, User
from app.db.queries.boards import BoardsQueries
from app.db.queries.notifications import NotificationsQueries


class BoardsService:
    def __init__(self, db: Session) -> None:
        self.q_b = BoardsQueries(db)
        self.q_n = NotificationsQueries(db)

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

    def get_my_boards_counts(self, *, members: list[BoardMember]) -> dict:
        return self.q_b.get_my_boards_counts(board_ids=[member.board.id for member in members])

    def get_board(self, *, current_user: User, board_id) -> BoardMember:
        member = self.q_b.get_by_id_for_user(board_id=board_id, user_id=current_user.id)

        if member is None:
            raise ValueError("Board not found")

        return member

    def join(self, *, current_user: User, board_id) -> BoardMember:
        board = self.q_b.get_by_id(board_id=board_id)
        if board is None:
            raise ValueError("Board not found")

        member = self.q_b.get_member(board_id=board_id, user_id=current_user.id)
        if member is not None:
            return member

        member = self.q_b.add_member(board_id=board_id, user_id=current_user.id, role="member")
        member.board = board
        self.q_n.create(
            user_id=current_user.id,
            board_id=board_id,
            text=f"\u0412\u044b \u043f\u0440\u0438\u0441\u043e\u0435\u0434\u0438\u043d\u0438\u043b\u0438\u0441\u044c \u043a \u0434\u043e\u0441\u043a\u0435 {board.title}.",
        )
        return member
