from datetime import datetime
import uuid
from sqlalchemy import DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base


class Vote(Base):
    __tablename__ = "votes"
    __table_args__ = (UniqueConstraint("user_id", "voting_id", "idea_id", name="uq_vote"),)

    # РїРѕР»СЏ
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    voting_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("votings.id", ondelete="CASCADE"),
        nullable=False,
    )
    idea_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("ideas.id", ondelete="CASCADE"),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    # СЃРІСЏР·Рё
    user = relationship("User", back_populates="votes")
    voting = relationship("Voting", back_populates="votes")
    idea = relationship("Idea", back_populates="votes")
