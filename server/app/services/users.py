from sqlalchemy.orm import Session

from app.db.queries.users import UsersQueries
from app.db.models import User


class UsersService:
    def __init__(self, db: Session) -> None:
        self.q_users = UsersQueries(db)

    def check_username(self, *, username: str) -> bool:
        user = self.q_users.get_by_username(username)
        return user is None

    def update_me(
        self,
        *,
        current_user: User,
        username: str | None,
        name: str | None,
        photo_url: str | None,
    ) -> User:
        if username is not None and username != current_user.username:
            user = self.q_users.get_by_username(username)
            if user is not None:
                raise ValueError("Username already exists")

        return self.q_users.update_me(user=current_user, username=username, name=name, photo_url=photo_url)
