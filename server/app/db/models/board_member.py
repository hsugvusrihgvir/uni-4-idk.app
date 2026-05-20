from datetime import datetime
import uuid
from sqlalchemy import DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base


class UserBoard(Base):
    __tablename__ = "user_boards"
    __table_args__ = (UniqueConstraint("board_id", "user_id", name="uq_user_board"),)

    # РїРѕР»СЏ
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    board_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("boards.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    role_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user_roles.id"),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    # СЃРІСЏР·Рё
    board = relationship("Board", back_populates="members")
    user = relationship("User", back_populates="boards")
    user_role = relationship("UserRole", back_populates="user_boards")

    @property
    def role(self) -> str:
        return self.user_role.role


BoardMember = UserBoard
