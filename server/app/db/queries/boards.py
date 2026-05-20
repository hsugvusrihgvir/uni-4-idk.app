from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db.models import Board, BoardMember, Idea, UserRole


class BoardsQueries:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        *,
        title: str,
        description: str | None,
        moderation: bool,
        anon_ideas: bool,
    ) -> Board:
        board = Board(
            title=title,
            description=description,
            moderation=moderation,
            anon_ideas=anon_ideas,
        )

        self.db.add(board)
        self.db.flush()

        return board

    def add_member(
        self,
        *,
        board_id: UUID,
        user_id: UUID,
        role: str,
    ) -> BoardMember:
        r = self.get_or_create_role(role=role)

        member = BoardMember(board_id=board_id, user_id=user_id, role_id=r.id, user_role=r)

        self.db.add(member)
        self.db.flush()

        return member

    def get_or_create_role(self, *, role: str) -> UserRole:
        stmt = select(UserRole).where(UserRole.role == role).limit(1)
        r = self.db.execute(stmt).scalar_one_or_none()

        if r is not None:
            return r

        r = UserRole(role=role)

        self.db.add(r)
        self.db.flush()

        return r

    def get_member(self, *, board_id: UUID, user_id: UUID) -> BoardMember | None:
        stmt = (
            select(BoardMember)
            .options(selectinload(BoardMember.board), selectinload(BoardMember.user_role))
            .where(
                BoardMember.board_id == board_id,
                BoardMember.user_id == user_id,
            )
            .limit(1)
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def get_my_boards(self, *, user_id: UUID) -> list[BoardMember]:
        stmt = (
            select(BoardMember)
            .options(
                selectinload(BoardMember.board),
                selectinload(BoardMember.user_role),
            )
            .where(BoardMember.user_id == user_id)
            .order_by(BoardMember.created_at.desc())
        )
        return list(self.db.execute(stmt).scalars().all())

    def get_by_id_for_user(self, *, board_id: UUID, user_id: UUID) -> BoardMember | None:
        stmt = (
            select(BoardMember)
            .options(
                selectinload(BoardMember.board)
                .selectinload(Board.ideas)
                .selectinload(Idea.idea_status),
                selectinload(BoardMember.user_role),
            )
            .where(
                BoardMember.board_id == board_id,
                BoardMember.user_id == user_id,
            )
            .limit(1)
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def delete(self, board: Board) -> None:
        self.db.delete(board)
        self.db.flush()

    def update(
        self,
        *,
        board: Board,
        title: str | None,
        description: str | None,
        moderation: bool | None,
        anon_ideas: bool | None,
    ) -> Board:
        if title is not None:
            board.title = title
        if description is not None:
            board.description = description
        if moderation is not None:
            board.moderation = moderation
        if anon_ideas is not None:
            board.anon_ideas = anon_ideas

        self.db.flush()
        return board

    def get_members(self, *, board_id: UUID) -> list[BoardMember]:
        stmt = (
            select(BoardMember)
            .options(
                selectinload(BoardMember.user),
                selectinload(BoardMember.user_role),
            )
            .where(BoardMember.board_id == board_id)
        )
        return list(self.db.execute(stmt).scalars().all())

    def update_member_role(self, *, member: BoardMember, role: str) -> BoardMember:
        r = self.get_or_create_role(role=role)
        member.role_id = r.id
        member.user_role = r

        self.db.flush()
        return member

    def delete_member(self, member: BoardMember) -> None:
        self.db.delete(member)
        self.db.flush()
