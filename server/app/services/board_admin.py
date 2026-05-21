from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models import Board, BoardMember, User
from app.db.queries.boards import BoardsQueries
from app.db.queries.notifications import NotificationsQueries
from app.db.queries.users import UsersQueries


class BoardAdminService:
    def __init__(self, db: Session) -> None:
        self.q_b = BoardsQueries(db)
        self.q_u = UsersQueries(db)
        self.q_n = NotificationsQueries(db)

    def update(
        self,
        *,
        cur: User,
        board_id: UUID,
        title: str | None,
        description: str | None,
        moderation: bool | None,
        anon_ideas: bool | None,
    ) -> Board:
        m = self._admin(cur=cur, board_id=board_id, msg="Only admin can update board")
        return self.q_b.update(board=m.board, title=title, description=description, moderation=moderation, anon_ideas=anon_ideas)

    def delete_board(self, *, cur: User, board_id: UUID) -> None:
        m = self._admin(cur=cur, board_id=board_id, msg="Only admin can delete board")
        self.q_b.delete(m.board)

    def members(self, *, cur: User, board_id: UUID) -> list[BoardMember]:
        self._member(cur=cur, board_id=board_id)
        return self.q_b.get_members(board_id=board_id)

    def add_member(self, *, cur: User, board_id: UUID, username: str, role: str) -> BoardMember:
        admin = self._admin(cur=cur, board_id=board_id, msg="Only admin can add members")

        user = self.q_u.get_by_username(username)
        if user is None:
            raise ValueError("User not found")

        if self.q_b.get_member(board_id=board_id, user_id=user.id) is not None:
            raise ValueError("User already in board")

        member = self.q_b.add_member(board_id=board_id, user_id=user.id, role=role)
        self.q_n.create(
            user_id=user.id,
            board_id=board_id,
            text=f"\u0412\u0430\u0441 \u043f\u0440\u0438\u0433\u043b\u0430\u0441\u0438\u043b\u0438 \u043d\u0430 \u0434\u043e\u0441\u043a\u0443 {admin.board.title}.",
        )
        return member

    def change_role(self, *, cur: User, board_id: UUID, user_id: UUID, role: str) -> BoardMember:
        self._admin(cur=cur, board_id=board_id, msg="Only admin can change roles")
        target = self._target(board_id=board_id, user_id=user_id)

        if target.role == "admin" and role != "admin":
            self._check_last_admin(board_id)

        return self.q_b.update_member_role(member=target, role=role)

    def delete_member(self, *, cur: User, board_id: UUID, user_id: UUID) -> None:
        self._admin(cur=cur, board_id=board_id, msg="Only admin can delete members")
        target = self._target(board_id=board_id, user_id=user_id)

        if target.role == "admin":
            self._check_last_admin(board_id)

        self.q_b.delete_member(target)

    def _member(self, *, cur: User, board_id: UUID) -> BoardMember:
        m = self.q_b.get_member(board_id=board_id, user_id=cur.id)
        if m is None:
            raise ValueError("Board not found")
        return m

    def _admin(self, *, cur: User, board_id: UUID, msg: str) -> BoardMember:
        m = self._member(cur=cur, board_id=board_id)
        if m.role != "admin":
            raise PermissionError(msg)
        return m

    def _target(self, *, board_id: UUID, user_id: UUID) -> BoardMember:
        m = self.q_b.get_member(board_id=board_id, user_id=user_id)
        if m is None:
            raise ValueError("Member not found")
        return m

    def _check_last_admin(self, board_id: UUID) -> None:
        admins = [m for m in self.q_b.get_members(board_id=board_id) if m.role == "admin"]
        if len(admins) <= 1:
            raise ValueError("Board must have at least one admin")
