from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Notification


class NotificationsQueries:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_user(self, *, user_id: UUID) -> list[Notification]:
        stmt = (
            select(Notification)
            .where(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
        )
        return list(self.db.execute(stmt).scalars().all())

    def get_by_id(self, *, notification_id: UUID) -> Notification | None:
        stmt = select(Notification).where(Notification.id == notification_id).limit(1)
        return self.db.execute(stmt).scalar_one_or_none()

    def create(self, *, user_id: UUID, text: str, board_id: UUID | None = None) -> Notification:
        notif = Notification(user_id=user_id, board_id=board_id, text=text)
        self.db.add(notif)
        self.db.flush()
        return notif

    def delete(self, notification: Notification) -> None:
        self.db.delete(notification)
        self.db.flush()
