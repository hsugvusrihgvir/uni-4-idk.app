from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db.models import Idea, IdeaStatus


class IdeasQueries:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        *,
        board_id: UUID,
        user_id: UUID,
        title: str,
        description: str | None,
        status: str,
        is_anonymous: bool,
    ) -> Idea:
        st = self.get_or_create_status(status=status)

        idea = Idea(
            id_board=board_id,
            id_user=user_id,
            id_status=st.id,
            idea_status=st,
            title=title,
            description=description,
            is_anonymous=is_anonymous,
        )

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
            .where(Idea.id_board == board_id)
            .order_by(Idea.created_at.desc())
        )
        return list(self.db.execute(stmt).scalars().all())
