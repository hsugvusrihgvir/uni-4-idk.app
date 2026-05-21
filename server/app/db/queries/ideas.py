from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db.models import Idea, IdeaStatus


class IdeasQueries:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self, *,
        board_id: UUID,
        user_id: UUID,
        title: str,
        description: str | None,
        status: str,
        is_anonymous: bool,
    ) -> Idea:
        st = self.get_or_create_status(status=status)

        idea = Idea(
            board_id=board_id,
            user_id=user_id,
            status_id=st.id,
            title=title,
            description=description,
            is_anonymous=is_anonymous,
        )
        idea.idea_status = st

        self.db.add(idea)
        self.db.flush()

        return idea

    def get_or_create_status(self, *, status: str) -> IdeaStatus:
        stmt = select(IdeaStatus).where(IdeaStatus.status == status).limit(1)
        st = self.db.execute(stmt).scalar_one_or_none()

        if st is not None:
            return st

        st = IdeaStatus(status=status)

        self.db.add(st)
        self.db.flush()

        return st

    def get_by_board(self, *, board_id: UUID) -> list[Idea]:
        stmt = (
            select(Idea)
            .options(selectinload(Idea.idea_status))
            .where(Idea.board_id == board_id)
            .order_by(Idea.created_at.desc())
        )
        return list(self.db.execute(stmt).scalars().all())

    def get_by_board_and_status(self, *, board_id: UUID, status: str) -> list[Idea]:
        stmt = (
            select(Idea)
            .join(IdeaStatus)
            .options(selectinload(Idea.idea_status))
            .where(
                Idea.board_id == board_id,
                IdeaStatus.status == status,
            )
            .order_by(Idea.created_at.desc())
        )
        return list(self.db.execute(stmt).scalars().all())

    def get_by_id(self, *, idea_id: UUID) -> Idea | None:
        stmt = select(Idea).where(Idea.id == idea_id).limit(1)
        return self.db.execute(stmt).scalar_one_or_none()

    def delete(self, idea: Idea) -> None:
        self.db.delete(idea)
        self.db.flush()

    def update_status(self, *, idea: Idea, status: str) -> Idea:
        st = self.get_or_create_status(status=status)
        idea.status_id = st.id
        idea.idea_status = st

        self.db.flush()
        return idea
