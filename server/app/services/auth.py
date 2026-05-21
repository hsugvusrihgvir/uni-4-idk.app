import random
from uuid import UUID

from jose import JWTError
from sqlalchemy.orm import Session

from app.core.send_code import send_auth_code
from app.core.security import create_access_token, create_refresh_token, validate_refresh_token
from app.db.models import User
from app.db.queries.auth import AuthQueries
from app.db.queries.users import UsersQueries


mail_sender = send_auth_code


def gen_code() -> str:
    return str(random.randint(100000, 999999))


class AuthService:
    def __init__(self, db: Session) -> None:
        self.q_a = AuthQueries(db)
        self.q_u = UsersQueries(db)

    def login(self, *, email: str) -> bool:
        user = self.q_u.get_by_email(email)
        if user is None:
            return False

        code = gen_code()
        self.q_a.create_code(email=email, code=code, ttl_minutes=5)

        # mail_sender(email, code)
        print(f"[AUTH CODE] {email}: {code}")

        return True

    def register(self, *, email: str, username: str, name: str | None, photo_url: str | None) -> None:
        if self.q_u.get_by_email(email) is not None:
            raise ValueError("User already exists")

        if self.q_u.get_by_username(username) is not None:
            raise ValueError("Username already exists")

        self.q_u.create(email=email, username=username, name=name, photo_url=photo_url)

        code = gen_code()
        self.q_a.create_code(email=email, code=code, ttl_minutes=5)

        # mail_sender(email, code)
        print(f"[AUTH CODE] {email}: {code}")

    def verify(self, *, email: str, code: str) -> tuple[str, str, User]:
        row = self.q_a.get_last_code(email=email, code=code)
        if row is None:
            raise ValueError("Invalid or expired code")

        self.q_a.use_code(row)

        user = self.q_u.get_by_email(email)
        if user is None:
            raise ValueError("User not found")

        access = create_access_token(str(user.id))
        refresh = create_refresh_token(str(user.id))
        return access, refresh, user

    def refresh(self, *, refresh_token: str) -> str:
        try:
            user_id = UUID(validate_refresh_token(refresh_token))
        except (JWTError, ValueError):
            raise ValueError("Invalid refresh token")

        user = self.q_u.get_by_id(user_id)
        if user is None:
            raise ValueError("User not found")

        return create_access_token(str(user.id))
