from datetime import datetime
import uuid
from sqlalchemy import DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base


class Vote(Base):
    __tablename__ = "votes"
    __table_args__ = (UniqueConstraint("id_user", "id_voting", "id_idea", name="uq_vote"),)

    # поля
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    id_user: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    id_voting: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("votings.id", ondelete="CASCADE"),
        nullable=False,
    )
    id_idea: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("ideas.id", ondelete="CASCADE"),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    # связи
    user = relationship("User", back_populates="votes")
    voting = relationship("Voting", back_populates="votes")
    idea = relationship("Idea", back_populates="votes")
