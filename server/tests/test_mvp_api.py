from datetime import datetime, timezone
from types import SimpleNamespace
from uuid import UUID
import pytest

from app.api import auth as auth_api
from app.api import boards as boards_api
from app.api import ideas as ideas_api
from app.api import telegram as telegram_api
from app.api import users as users_api
from app.api import votings as votings_api


class FakeAuthService:
    exists = True
    register_error = None
    verify_error = None
    refresh_error = None

    def __init__(self, db):
        pass

    def login(self, *, email):
        return self.exists

    def register(self, **kwargs):
        if self.register_error:
            raise ValueError(self.register_error)

    def verify(self, *, email, code):
        if self.verify_error:
            raise ValueError(self.verify_error)

        user = SimpleNamespace(
            email=email,
            username="username",
            name="User",
            photo_url="photo.png",
        )
        return "access_token", "refresh_token", user

    def refresh(self, *, refresh_token):
        if self.refresh_error:
            raise ValueError(self.refresh_error)

        return "new_access_token"


class FakeUsersService:
    available = True
    update_error = None

    def __init__(self, db):
        pass

    def check_username(self, *, username):
        return self.available

    def update_me(self, *, current_user, username, name, photo_url):
        if self.update_error:
            raise ValueError(self.update_error)

        return SimpleNamespace(
            email=current_user.email,
            username=username,
            name=name,
            photo_url=photo_url,
        )


class FakeBoardsService:
    get_error = None

    def __init__(self, db):
        pass

    def create(self, *, current_user, title, description, moderation, anon_ideas):
        return SimpleNamespace(
            id=UUID("22222222-2222-2222-2222-222222222222"),
            title=title,
            description=description,
            moderation=moderation,
            anon_ideas=anon_ideas,
        )

    def get_my_boards(self, *, current_user):
        board = SimpleNamespace(
            id=UUID("22222222-2222-2222-2222-222222222222"),
            title="Board 1",
            description="description",
        )
        return [SimpleNamespace(board=board, role="admin")]

    def get_my_boards_counts(self, *, members):
        return {
            UUID("22222222-2222-2222-2222-222222222222"): {
                "ideas_count": 1,
                "members_count": 2,
            }
        }

    def get_board(self, *, current_user, board_id):
        if self.get_error:
            raise ValueError(self.get_error)

        idea = SimpleNamespace(
            id=UUID("33333333-3333-3333-3333-333333333333"),
            title="Idea 1",
            description="description",
            status="approved",
        )
        board = SimpleNamespace(
            id=board_id,
            title="Board 1",
            description="description",
            anon_ideas=True,
            moderation=False,
            created_at=datetime(2000, 1, 1, tzinfo=timezone.utc),
            ideas=[idea],
        )
        return SimpleNamespace(board=board, role="admin")


class FakeIdeasService:
    create_error = None
    list_error = None

    def __init__(self, db):
        pass

    def create(self, *, current_user, board_id, title, description, is_anonymous):
        if self.create_error:
            raise ValueError(self.create_error)

        return SimpleNamespace(
            id=UUID("33333333-3333-3333-3333-333333333333"),
            board_id=board_id,
            title=title,
            description=description,
            status="pending",
            is_anonymous=is_anonymous,
            created_at=datetime(2000, 1, 1, tzinfo=timezone.utc),
        )

    def get_by_board(self, *, current_user, board_id):
        if self.list_error:
            raise ValueError(self.list_error)

        idea = SimpleNamespace(
            id=UUID("33333333-3333-3333-3333-333333333333"),
            board_id=board_id,
            title="Idea 1",
            description="description",
            status="approved",
            is_anonymous=True,
            created_at=datetime(2000, 1, 1, tzinfo=timezone.utc),
        )
        return [idea]


class FakeVotingsService:
    get_error = None
    vote_error = None
    delete_vote_error = None
    results_error = None

    def __init__(self, db):
        pass

    def get_by_board(self, *, current_user, board_id):
        if self.get_error:
            raise ValueError(self.get_error)

        return [
            SimpleNamespace(
                id=UUID("44444444-4444-4444-4444-444444444444"),
                board_id=board_id,
                voting_type=SimpleNamespace(type="yes_no"),
                created_at=datetime(2000, 1, 1, tzinfo=timezone.utc),
            )
        ]

    def vote(self, *, current_user, voting_id, idea_id):
        if self.vote_error:
            raise ValueError(self.vote_error)

        return SimpleNamespace(
            id=UUID("55555555-5555-5555-5555-555555555555"),
            voting_id=voting_id,
            idea_id=idea_id,
            created_at=datetime(2000, 1, 1, tzinfo=timezone.utc),
        )

    def delete_vote(self, *, current_user, voting_id, idea_id):
        if self.delete_vote_error:
            raise ValueError(self.delete_vote_error)

    def get_results(self, *, current_user, voting_id):
        if self.results_error:
            raise ValueError(self.results_error)

        return [
            {
                "idea_id": UUID("33333333-3333-3333-3333-333333333333"),
                "title": "Idea 1",
                "votes_count": 3,
                "approval_percent": 100,
                "user_voted": True,
            }
        ]


class FakeVotingAdminService:
    create_error = None
    delete_error = None

    def __init__(self, db):
        pass

    def create(self, *, cur, board_id, type):
        if self.create_error:
            raise ValueError(self.create_error)

        return SimpleNamespace(
            id=UUID("44444444-4444-4444-4444-444444444444"),
            board_id=board_id,
            voting_type=SimpleNamespace(type=type),
            created_at=datetime(2000, 1, 1, tzinfo=timezone.utc),
        )

    def delete(self, *, cur, voting_id):
        if self.delete_error:
            raise ValueError(self.delete_error)


class FakeTelegramService:
    link_code = "123456"
    link_error = None
    bind_error = None
    idea_error = None

    def __init__(self, db):
        pass

    def create_link_code(self, *, current_user):
        return self.link_code

    def link_user(self, *, code, telegram_user_id):
        if self.link_error:
            raise ValueError(self.link_error)

        return SimpleNamespace(id=UUID("11111111-1111-1111-1111-111111111111"))

    def bind_chat(self, *, board_id, telegram_user_id, telegram_chat_id, chat_title):
        if self.bind_error:
            raise ValueError(self.bind_error)

        return SimpleNamespace(
            board_id=board_id,
            telegram_chat_id=telegram_chat_id,
            chat_title=chat_title,
        )

    def create_idea_from_chat(self, *, telegram_user_id, telegram_chat_id, text):
        if self.idea_error:
            raise ValueError(self.idea_error)

        return SimpleNamespace(
            id=UUID("33333333-3333-3333-3333-333333333333"),
            board_id=UUID("22222222-2222-2222-2222-222222222222"),
            title=text,
            description=None,
            status="pending",
            is_anonymous=False,
            author_username="username",
            author_name="User",
            created_at=datetime(2000, 1, 1, tzinfo=timezone.utc),
        )


@pytest.fixture(autouse=True)
def services(monkeypatch):
    FakeAuthService.exists = True
    FakeAuthService.register_error = None
    FakeAuthService.verify_error = None
    FakeAuthService.refresh_error = None
    FakeUsersService.available = True
    FakeUsersService.update_error = None
    FakeBoardsService.get_error = None
    FakeIdeasService.create_error = None
    FakeIdeasService.list_error = None
    FakeVotingsService.get_error = None
    FakeVotingsService.vote_error = None
    FakeVotingsService.delete_vote_error = None
    FakeVotingsService.results_error = None
    FakeVotingAdminService.create_error = None
    FakeVotingAdminService.delete_error = None
    FakeTelegramService.link_error = None
    FakeTelegramService.bind_error = None
    FakeTelegramService.idea_error = None

    monkeypatch.setattr(auth_api, "AuthService", FakeAuthService)
    monkeypatch.setattr(users_api, "UsersService", FakeUsersService)
    monkeypatch.setattr(boards_api, "BoardsService", FakeBoardsService)
    monkeypatch.setattr(boards_api, "IdeasService", FakeIdeasService)
    monkeypatch.setattr(ideas_api, "IdeasService", FakeIdeasService)
    monkeypatch.setattr(votings_api, "VotingsService", FakeVotingsService)
    monkeypatch.setattr(votings_api, "VotingAdminService", FakeVotingAdminService)
    monkeypatch.setattr(telegram_api, "TelegramService", FakeTelegramService)
    monkeypatch.setenv("TELEGRAM_BOT_SECRET", "secret")


@pytest.mark.parametrize(
    "exists, expected_status",
    [
        (True, 200),
        (False, 200),
    ]
)
def test_login(client, exists, expected_status):
    FakeAuthService.exists = exists

    response = client.post("/api/v1/auth/login", json={"email": "user@example.com"})

    assert response.status_code == expected_status
    assert response.json()["exists"] == exists


@pytest.mark.parametrize(
    "error, expected_status",
    [
        (None, 200),
        ("User already exists", 400),
    ]
)
def test_register(client, error, expected_status):
    FakeAuthService.register_error = error

    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "user@example.com",
            "username": "username",
            "name": "User",
            "photo_url": "photo.png",
        }
    )

    assert response.status_code == expected_status

    if expected_status == 200:
        assert "message" in response.json()
    else:
        assert response.json() == {"detail": error}


def test_verify(client):
    response = client.post(
        "/api/v1/auth/verify",
        json={"email": "user@example.com", "code": "123456"}
    )

    assert response.status_code == 200
    assert response.json()["access_token"] == "access_token"
    assert response.json()["refresh_token"] == "refresh_token"
    assert response.json()["token_type"] == "bearer"
    assert response.json()["user"]["email"] == "user@example.com"


def test_verify_error(client):
    FakeAuthService.verify_error = "Invalid or expired code"

    response = client.post(
        "/api/v1/auth/verify",
        json={"email": "user@example.com", "code": "123456"}
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid or expired code"}


def test_refresh(client):
    response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": "refresh_token"}
    )

    assert response.status_code == 200
    assert response.json() == {
        "access_token": "new_access_token",
        "token_type": "bearer",
    }


@pytest.mark.parametrize(
    "available",
    [
        True,
        False,
    ]
)
def test_check_username(client, available):
    FakeUsersService.available = available

    response = client.get("/api/v1/users/check-username?username=rin")

    assert response.status_code == 200
    assert response.json()["available"] == available


def test_get_me(client):
    response = client.get("/api/v1/users/me")

    assert response.status_code == 200
    assert response.json() == {
        "email": "user@example.com",
        "username": "username",
        "name": "User",
        "photo_url": "photo.png",
        "tg_id": None,
    }


def test_update_me(client):
    response = client.patch(
        "/api/v1/users/me",
        json={"username": "newname", "name": "New", "photo_url": "new.png"}
    )

    assert response.status_code == 200
    assert response.json()["username"] == "newname"
    assert response.json()["name"] == "New"


def test_create_board(client):
    response = client.post(
        "/api/v1/boards",
        json={
            "title": "Title",
            "description": "description",
            "moderation": False,
            "anon_ideas": True,
        }
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": "22222222-2222-2222-2222-222222222222",
        "title": "Title",
        "description": "description",
        "moderation": False,
        "anon_ideas": True,
    }


def test_get_boards(client):
    response = client.get("/api/v1/boards")

    assert response.status_code == 200
    assert response.json() == {
        "items": [
                {
                    "id": "22222222-2222-2222-2222-222222222222",
                    "title": "Board 1",
                    "description": "description",
                    "role": "admin",
                    "ideas_count": 1,
                    "members_count": 2,
                }
            ]
        }


@pytest.mark.parametrize(
    "error, expected_status",
    [
        (None, 200),
        ("Board not found", 404),
    ]
)
def test_get_board(client, error, expected_status):
    FakeBoardsService.get_error = error

    response = client.get("/api/v1/boards/22222222-2222-2222-2222-222222222222")

    assert response.status_code == expected_status

    if expected_status == 200:
        assert response.json()["title"] == "Board 1"
        assert response.json()["role"] == "admin"
        assert response.json()["ideas"][0]["status"] == "approved"
    else:
        assert response.json() == {"detail": error}


def test_create_idea(client):
    response = client.post(
        "/api/v1/ideas",
        json={
            "board_id": "22222222-2222-2222-2222-222222222222",
            "title": "Title",
            "description": "description",
            "is_anonymous": True,
        }
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Title"
    assert response.json()["status"] == "pending"
    assert response.json()["is_anonymous"] is True


def test_create_idea_error(client):
    FakeIdeasService.create_error = "Anonymous ideas are disabled"

    response = client.post(
        "/api/v1/ideas",
        json={
            "board_id": "22222222-2222-2222-2222-222222222222",
            "title": "Title",
            "description": "description",
            "is_anonymous": True,
        }
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Anonymous ideas are disabled"}


def test_get_board_ideas(client):
    response = client.get("/api/v1/boards/22222222-2222-2222-2222-222222222222/ideas")

    assert response.status_code == 200
    assert response.json()["items"][0]["title"] == "Idea 1"
    assert response.json()["items"][0]["status"] == "approved"


def test_create_voting(client):
    response = client.post(
        "/api/v1/boards/22222222-2222-2222-2222-222222222222/votings",
        json={"type": "yes_no"},
    )

    assert response.status_code == 200
    assert response.json()["type"] == "yes_no"


def test_get_board_votings(client):
    response = client.get("/api/v1/boards/22222222-2222-2222-2222-222222222222/votings")

    assert response.status_code == 200
    assert response.json()["items"][0]["type"] == "yes_no"


def test_delete_voting(client):
    response = client.delete("/api/v1/votings/44444444-4444-4444-4444-444444444444")

    assert response.status_code == 204


def test_create_vote(client):
    response = client.post(
        "/api/v1/votes",
        json={
            "voting_id": "44444444-4444-4444-4444-444444444444",
            "idea_id": "33333333-3333-3333-3333-333333333333",
        },
    )

    assert response.status_code == 200
    assert response.json()["idea_id"] == "33333333-3333-3333-3333-333333333333"


def test_delete_vote(client):
    response = client.request(
        "DELETE",
        "/api/v1/votes",
        json={
            "voting_id": "44444444-4444-4444-4444-444444444444",
            "idea_id": "33333333-3333-3333-3333-333333333333",
        },
    )

    assert response.status_code == 204


def test_get_voting_results(client):
    response = client.get("/api/v1/votings/44444444-4444-4444-4444-444444444444/results")

    assert response.status_code == 200
    item = response.json()["items"][0]
    assert item["votes_count"] == 3
    assert item["approval_percent"] == 100
    assert item["user_voted"] is True


def test_create_telegram_link_code(client):
    response = client.post("/api/v1/telegram/link-code")

    assert response.status_code == 200
    assert response.json() == {"code": "123456"}


def test_link_telegram_user_requires_secret(client):
    response = client.post(
        "/api/v1/telegram/users/link",
        json={"code": "123456", "telegram_user_id": 123},
    )

    assert response.status_code == 403


def test_link_telegram_user(client):
    response = client.post(
        "/api/v1/telegram/users/link",
        headers={"X-Bot-Secret": "secret"},
        json={"code": "123456", "telegram_user_id": 123},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Telegram account linked"


def test_bind_telegram_chat(client):
    response = client.post(
        "/api/v1/telegram/chats/bind",
        headers={"X-Bot-Secret": "secret"},
        json={
            "board_id": "22222222-2222-2222-2222-222222222222",
            "telegram_user_id": 123,
            "telegram_chat_id": -100123,
            "chat_title": "Chat",
        },
    )

    assert response.status_code == 200
    assert response.json()["telegram_chat_id"] == -100123


def test_create_telegram_idea(client):
    response = client.post(
        "/api/v1/telegram/ideas",
        headers={"X-Bot-Secret": "secret"},
        json={
            "telegram_user_id": 123,
            "telegram_chat_id": -100123,
            "text": "Idea from chat",
        },
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Idea from chat"
    assert response.json()["status"] == "pending"
