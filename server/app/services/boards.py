from uuid import UUID

from sqlalchemy.orm import Session

from app.db.queries.boards import BoardsQueries
from app.db.queries.users import UsersQueries
from app.db.models import Board, BoardMember, User


class BoardsService:
    def __init__(self, db: Session) -> None:
        self.q_boards = BoardsQueries(db)
        self.q_users = UsersQueries(db)

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

    def update(
        self,
        *,
        current_user: User,
        board_id: UUID,
        title: str | None,
        description: str | None,
        moderation: bool | None,
        anon_ideas: bool | None,
    ) -> Board:
        member = self.q_boards.get_member(board_id=board_id, user_id=current_user.id)

        if member is None:
            raise ValueError("Board not found")

        if member.role != "admin":
            raise PermissionError("Only admin can update board")

        return self.q_boards.update(
            board=member.board,
            title=title,
            description=description,
            moderation=moderation,
            anon_ideas=anon_ideas,
        )

    def get_members(self, *, current_user: User, board_id: UUID) -> list[BoardMember]:
        member = self.q_boards.get_member(board_id=board_id, user_id=current_user.id)

        if member is None:
            raise ValueError("Board not found")

        return self.q_boards.get_members(board_id=board_id)

    def add_member(self, *, current_user: User, board_id: UUID, username: str, role: str) -> BoardMember:
        member = self.q_boards.get_member(board_id=board_id, user_id=current_user.id)

        if member is None:
            raise ValueError("Board not found")

        if member.role != "admin":
            raise PermissionError("Only admin can add members")

        user = self.q_users.get_by_username(username)
        if user is None:
            raise ValueError("User not found")

        exists = self.q_boards.get_member(board_id=board_id, user_id=user.id)
        if exists is not None:
            raise ValueError("User already in board")

        return self.q_boards.add_member(board_id=board_id, user_id=user.id, role=role)

    def change_member_role(self, *, current_user: User, board_id: UUID, user_id: UUID, role: str) -> BoardMember:
        member = self.q_boards.get_member(board_id=board_id, user_id=current_user.id)

        if member is None:
            raise ValueError("Board not found")

        if member.role != "admin":
            raise PermissionError("Only admin can change roles")

        target = self.q_boards.get_member(board_id=board_id, user_id=user_id)
        if target is None:
            raise ValueError("Member not found")

        if target.role == "admin" and role != "admin":
            admins = [item for item in self.q_boards.get_members(board_id=board_id) if item.role == "admin"]
            if len(admins) <= 1:
                raise ValueError("Board must have at least one admin")

        return self.q_boards.update_member_role(member=target, role=role)

    def delete_member(self, *, current_user: User, board_id: UUID, user_id: UUID) -> None:
        member = self.q_boards.get_member(board_id=board_id, user_id=current_user.id)

        if member is None:
            raise ValueError("Board not found")

        if member.role != "admin":
            raise PermissionError("Only admin can delete members")

        target = self.q_boards.get_member(board_id=board_id, user_id=user_id)
        if target is None:
            raise ValueError("Member not found")

        if target.role == "admin":
            admins = [item for item in self.q_boards.get_members(board_id=board_id) if item.role == "admin"]
            if len(admins) <= 1:
                raise ValueError("Board must have at least one admin")

        self.q_boards.delete_member(target)
