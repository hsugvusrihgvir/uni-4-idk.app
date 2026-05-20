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

        member = BoardMember(id_board=board_id, id_user=user_id, id_role=r.id, user_role=r)

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
                BoardMember.id_board == board_id,
                BoardMember.id_user == user_id,
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
            .where(BoardMember.id_user == user_id)
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
                BoardMember.id_board == board_id,
                BoardMember.id_user == user_id,
            )
            .limit(1)
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def delete(self, board: Board) -> None:
        self.db.delete(board)
        self.db.flush()
