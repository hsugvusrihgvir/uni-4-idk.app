from datetime import datetime
import uuid
from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base


class Voting(Base):
    __tablename__ = "votings"

    # поля
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    id_type: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("voting_types.id"),
        nullable=False,
    )
    id_board: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("boards.id", ondelete="CASCADE"),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    # связи
    voting_type = relationship("VotingType", back_populates="votings")
    board = relationship("Board", back_populates="votings")

    votes = relationship(
        "Vote",
        back_populates="voting",
        cascade="all, delete-orphan",
    )
