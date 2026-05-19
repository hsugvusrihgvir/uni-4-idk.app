from datetime import datetime
import uuid
from sqlalchemy import Boolean, DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base


class Board(Base):
    __tablename__ = "boards"

    # поля
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    moderation: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    anon_ideas: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    # связи
    members = relationship(
        "UserBoard",
        back_populates="board",
        cascade="all, delete-orphan",
    )

    ideas = relationship(
        "Idea",
        back_populates="board",
        cascade="all, delete-orphan",
    )

    votings = relationship(
        "Voting",
        back_populates="board",
        cascade="all, delete-orphan",
    )

    notifications = relationship(
        "Notification",
        back_populates="board",
        cascade="all, delete-orphan",
    )
