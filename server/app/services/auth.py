import random
from uuid import UUID

from jose import JWTError
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    create_refresh_token,
    validate_refresh_token,
)
from app.db.queries.auth import AuthQueries
from app.db.queries.users import UsersQueries
from app.db.models import User


# код на почту
def _generate_code() -> str:
    return str(random.randint(100000, 999999))


class AuthService:
    def __init__(self, db: Session) -> None:
        self.q_auth = AuthQueries(db)
        self.q_users = UsersQueries(db)

    def login(self, *, email: str) -> bool:
        user = self.q_users.get_by_email(email)

        if user is None:
            return False

        code = _generate_code()
        self.q_auth.create_code(email=email, code=code, ttl_minutes=5)

        # заглушка УДАЛИТЬ
        print(f"[AUTH CODE] {email}: {code}")

        return True

    def register(
        self,
        *,
        email: str,
        username: str,
        name: str | None,
        photo_url: str | None,
    ) -> None:
        user = self.q_users.get_by_email(email)
        if user is not None:
            raise ValueError("User already exists")

        user = self.q_users.get_by_username(username)
        if user is not None:
            raise ValueError("Username already exists")

        self.q_users.create(email=email, username=username, name=name, photo_url=photo_url)

        code = _generate_code()
        self.q_auth.create_code(email=email, code=code, ttl_minutes=5)

        # заглушка УДАЛИТЬ
        print(f"[AUTH CODE] {email}: {code}")

    def verify(self, *, email: str, code: str) -> tuple[str, str, User]:
        email_code = self.q_auth.get_last_code(email=email, code=code)

        if email_code is None:
            raise ValueError("Invalid or expired code")

        self.q_auth.use_code(email_code)

        user = self.q_users.get_by_email(email)
        if user is None:
            raise ValueError("User not found")

        access_token = create_access_token(str(user.id))
        refresh_token = create_refresh_token(str(user.id))

        return access_token, refresh_token, user

    def refresh(self, *, refresh_token: str) -> str:
        try:
            user_id = UUID(validate_refresh_token(refresh_token))
        except (JWTError, ValueError):
            raise ValueError("Invalid refresh token")

        user = self.q_users.get_by_id(user_id)

        if user is None:
            raise ValueError("User not found")

        return create_access_token(str(user.id))
