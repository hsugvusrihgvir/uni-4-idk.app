from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models import Notification, User
from app.db.queries.notifications import NotificationsQueries


class NotificationsService:
    def __init__(self, db: Session) -> None:
        self.q_n = NotificationsQueries(db)

    def get_my(self, *, current_user: User) -> list[Notification]:
        return self.q_n.get_by_user(user_id=current_user.id)

    def delete(self, *, current_user: User, notification_id: UUID) -> None:
        notif = self.q_n.get_by_id(notification_id=notification_id)

        if notif is None:
            raise ValueError("Notification not found")

        if notif.user_id != current_user.id:
            raise PermissionError("Only owner can delete notification")

        self.q_n.delete(notif)
