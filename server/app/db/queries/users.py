from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import User


class UsersQueries:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, user_id: UUID) -> User | None:
        stmt = (
            select(User)
            .where(User.id == user_id)
            .limit(1)
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def get_by_email(self, email: str) -> User | None:
        stmt = (
            select(User)
            .where(User.email == email)
            .limit(1)
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def get_by_username(self, username: str) -> User | None:
        stmt = (
            select(User)
            .where(User.username == username)
            .limit(1)
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def get_by_tg_id(self, tg_id: int) -> User | None:
        stmt = (
            select(User)
            .where(User.tg_id == tg_id)
            .limit(1)
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def set_tg_id(self, *, user: User, tg_id: int) -> User:
        user.tg_id = tg_id
        self.db.flush()
        return user

    def create(
        self,
        *,
        email: str,
        username: str,
        name: str | None,
        photo_url: str | None,
    ) -> User:
        user = User(
            email=email,
            username=username,
            name=name,
            photo_url=photo_url,
        )

        self.db.add(user)
        self.db.flush()

        return user

    def update_me(
        self,
        *,
        user: User,
        username: str | None,
        name: str | None,
        photo_url: str | None,
    ) -> User:
        if username is not None:
            user.username = username
        if name is not None:
            user.name = name
        if photo_url is not None:
            user.photo_url = photo_url

        self.db.flush()

        return user
