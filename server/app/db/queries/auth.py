from datetime import datetime, timedelta, timezone
from uuid import UUID

from sqlalchemy import and_, desc, select, update
from sqlalchemy.orm import Session

from app.db.models import EmailCode, User


class AuthQueries:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_code(self, *, email: str, code: str, ttl_minutes: int = 5) -> EmailCode:
        now = datetime.now(timezone.utc)
        exp = now + timedelta(minutes=ttl_minutes)

        stmt = (
            update(EmailCode)
            .where(and_(EmailCode.email == email, EmailCode.is_used.is_(False)))
            .values(is_used=True)
        )
        self.db.execute(stmt)

        row = EmailCode(email=email, code=code, expires_at=exp, is_used=False)
        self.db.add(row)
        self.db.flush()

        return row

    def get_last_code(self, *, email: str, code: str) -> EmailCode | None:
        now = datetime.now(timezone.utc)
        stmt = (
            select(EmailCode)
            .where(
                and_(
                    EmailCode.email == email,
                    EmailCode.code == code,
                    EmailCode.is_used.is_(False),
                    EmailCode.expires_at > now,
                )
            )
            .order_by(desc(EmailCode.created_at), desc(EmailCode.id))
            .limit(1)
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def use_code(self, row: EmailCode) -> EmailCode:
        row.is_used = True
        self.db.flush()
        return row

    def get_user_by_email(self, *, email: str) -> User | None:
        stmt = select(User).where(User.email == email).limit(1)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_user_by_id(self, *, user_id: UUID) -> User | None:
        stmt = select(User).where(User.id == user_id).limit(1)
        return self.db.execute(stmt).scalar_one_or_none()
