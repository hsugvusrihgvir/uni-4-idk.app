from datetime import datetime, timedelta, timezone
from sqlalchemy import and_, desc, select, update
from sqlalchemy.orm import Session

from app.db.models import EmailCode, User


class AuthQueries:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_code(self, *, email: str, code: str, ttl_minutes: int = 5) -> EmailCode:
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(minutes=ttl_minutes)

        # удаляем предыдущие
        self.db.execute(update(EmailCode)
                        .where(and_(EmailCode.email == email,
                                    EmailCode.is_used.is_(False)))
                        .values(is_used=True) )

        email_code = EmailCode(
            email=email,
            code=code,
            expires_at=expires_at,
            is_used=False,
        )

        self.db.add(email_code)
        self.db.flush()

        return email_code

    def get_last_code(self, *, email: str, code: str) -> EmailCode | None:
        now = datetime.now(timezone.utc)

        stmt = (select(EmailCode)
                .where(and_(
                    EmailCode.email == email,
                    EmailCode.code == code,
                    EmailCode.is_used.is_(False),
                    EmailCode.expires_at > now,
                )
            ).order_by(desc(EmailCode.created_at),
                       desc(EmailCode.id)).limit(1))

        return self.db.execute(stmt).scalar_one_or_none()

    def use_code(self, email_code: EmailCode) -> EmailCode:
        email_code.is_used = True
        self.db.flush()

        return email_code

    def get_user_by_email(self, *, email: str) -> User | None:
        stmt = (
            select(User)
            .where(User.email == email)
            .limit(1)
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def get_user_by_id(self, *, user_id) -> User | None:
        stmt = (
            select(User)
            .where(User.id == user_id)
            .limit(1)
        )
        return self.db.execute(stmt).scalar_one_or_none()
