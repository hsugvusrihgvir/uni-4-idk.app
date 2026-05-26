from types import SimpleNamespace
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from app.core.deps import get_current_user
from app.db.session import get_db
from app.main import app


def fake_db():
    yield None


@pytest.fixture
def user():
    return SimpleNamespace(
        id=UUID("11111111-1111-1111-1111-111111111111"),
        email="user@example.com",
        username="username",
        name="User",
        photo_url="photo.png",
        tg_id=None,
    )


@pytest.fixture
def client(user):
    app.dependency_overrides[get_db] = fake_db
    app.dependency_overrides[get_current_user] = lambda: user

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
