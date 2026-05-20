from datetime import datetime, timedelta, timezone
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.db.models import (
    Base,
    Board,
    EmailCode,
    Idea,
    IdeaStatus,
    Notification,
    TgCode,
    User,
    UserBoard,
    UserRole,
    Vote,
    Voting,
    VotingType,
)
from app.db.session import SessionLocal, engine


ids = {
    "admin": UUID("10000000-0000-0000-0000-000000000001"),
    "moderator": UUID("10000000-0000-0000-0000-000000000002"),
    "member": UUID("10000000-0000-0000-0000-000000000003"),
    "pending": UUID("20000000-0000-0000-0000-000000000001"),
    "approved": UUID("20000000-0000-0000-0000-000000000002"),
    "rejected": UUID("20000000-0000-0000-0000-000000000003"),
    "like": UUID("30000000-0000-0000-0000-000000000001"),
    "yes_no": UUID("30000000-0000-0000-0000-000000000002"),
    "user_1": UUID("40000000-0000-0000-0000-000000000001"),
    "user_2": UUID("40000000-0000-0000-0000-000000000002"),
    "user_3": UUID("40000000-0000-0000-0000-000000000003"),
    "board_1": UUID("50000000-0000-0000-0000-000000000001"),
    "board_2": UUID("50000000-0000-0000-0000-000000000002"),
    "ub_1": UUID("60000000-0000-0000-0000-000000000001"),
    "ub_2": UUID("60000000-0000-0000-0000-000000000002"),
    "ub_3": UUID("60000000-0000-0000-0000-000000000003"),
    "ub_4": UUID("60000000-0000-0000-0000-000000000004"),
    "idea_1": UUID("70000000-0000-0000-0000-000000000001"),
    "idea_2": UUID("70000000-0000-0000-0000-000000000002"),
    "idea_3": UUID("70000000-0000-0000-0000-000000000003"),
    "voting_1": UUID("80000000-0000-0000-0000-000000000001"),
    "voting_2": UUID("80000000-0000-0000-0000-000000000002"),
    "vote_1": UUID("90000000-0000-0000-0000-000000000001"),
    "vote_2": UUID("90000000-0000-0000-0000-000000000002"),
    "notif_1": UUID("a0000000-0000-0000-0000-000000000001"),
    "notif_2": UUID("a0000000-0000-0000-0000-000000000002"),
    "email_code_1": UUID("b0000000-0000-0000-0000-000000000001"),
    "email_code_2": UUID("b0000000-0000-0000-0000-000000000002"),
    "tg_code_1": UUID("c0000000-0000-0000-0000-000000000001"),
    "tg_code_2": UUID("c0000000-0000-0000-0000-000000000002"),
}

seed_ids = list(ids.values())


def one(db: Session, model, field, value):
    return db.execute(select(model).where(field == value).limit(1)).scalar_one_or_none()


def add(db: Session, model, key: str, **data):
    obj = db.get(model, ids[key])
    if obj is not None:
        return obj

    obj = model(id=ids[key], **data)
    db.add(obj)
    return obj


def clear_seed_data(db: Session):
    for model in (Vote, Voting, Notification, TgCode, EmailCode, Idea, UserBoard, Board, User):
        db.execute(delete(model).where(model.id.in_(seed_ids)))

    for model in (VotingType, IdeaStatus, UserRole):
        db.execute(delete(model).where(model.id.in_(seed_ids)))

    db.flush()


def seed_dicts(db: Session):
    for key, role in {"admin": "admin", "moderator": "moderator", "member": "member"}.items():
        obj = one(db, UserRole, UserRole.role, role)
        if obj is None:
            obj = add(db, UserRole, key, role=role)
        ids[key] = obj.id

    for key, status in {"pending": "pending", "approved": "approved", "rejected": "rejected"}.items():
        obj = one(db, IdeaStatus, IdeaStatus.status, status)
        if obj is None:
            obj = add(db, IdeaStatus, key, status=status)
        ids[key] = obj.id

    for key, v_type in {"like": "like", "yes_no": "yes_no"}.items():
        obj = one(db, VotingType, VotingType.type, v_type)
        if obj is None:
            obj = add(db, VotingType, key, type=v_type)
        ids[key] = obj.id

    db.flush()


def seed_users(db: Session):
    users = [
        ("user_1", "dasha@example.com", "dasha", 100001, "\u0414\u0430\u0448\u0430", "photo-1.png"),
        ("user_2", "masha@example.com", "masha", 100002, "\u041c\u0430\u0448\u0430", "photo-2.png"),
        ("user_3", "katya@example.com", "katya", 100003, "\u041a\u0430\u0442\u044f", "photo-3.png"),
    ]

    for key, email, username, tg_id, name, photo_url in users:
        obj = one(db, User, User.email, email)
        if obj is None:
            obj = add(db, User, key, email=email, username=username, tg_id=tg_id, name=name, photo_url=photo_url)
        ids[key] = obj.id

    db.flush()


def seed_boards(db: Session):
    add(db, Board, "board_1", title="\u0414\u043e\u0441\u043a\u0430 1", description="\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u0434\u043e\u0441\u043a\u0438 1", moderation=True, anon_ideas=True)
    add(db, Board, "board_2", title="\u0414\u043e\u0441\u043a\u0430 2", description="\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u0434\u043e\u0441\u043a\u0438 2", moderation=False, anon_ideas=True)

    members = [
        ("ub_1", "board_1", "user_1", "admin"),
        ("ub_2", "board_1", "user_2", "moderator"),
        ("ub_3", "board_1", "user_3", "member"),
        ("ub_4", "board_2", "user_2", "admin"),
    ]

    for key, board, user, role in members:
        add(db, UserBoard, key, id_board=ids[board], id_user=ids[user], id_role=ids[role])

    db.flush()


def seed_ideas(db: Session):
    ideas = [
        ("idea_1", "board_1", "user_1", "approved", "\u0418\u0434\u0435\u044f 1", "\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u0438\u0434\u0435\u0438 1", True),
        ("idea_2", "board_1", "user_2", "pending", "\u0418\u0434\u0435\u044f 2", "\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u0438\u0434\u0435\u0438 2", False),
        ("idea_3", "board_2", "user_2", "approved", "\u0418\u0434\u0435\u044f 3", "\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u0438\u0434\u0435\u0438 3", False),
    ]

    for key, board, user, st, title, desc, anon in ideas:
        add(db, Idea, key, id_board=ids[board], id_user=ids[user], id_status=ids[st], title=title, description=desc, is_anonymous=anon)

    db.flush()


def seed_votings(db: Session):
    add(db, Voting, "voting_1", id_type=ids["yes_no"], id_board=ids["board_1"])
    add(db, Voting, "voting_2", id_type=ids["like"], id_board=ids["board_2"])

    votes = [
        ("vote_1", "user_2", "voting_1", "idea_1"),
        ("vote_2", "user_3", "voting_1", "idea_1"),
    ]

    for key, user, voting, idea in votes:
        add(db, Vote, key, id_user=ids[user], id_voting=ids[voting], id_idea=ids[idea])

    db.flush()


def seed_messages(db: Session):
    now = datetime.now(timezone.utc)

    add(db, Notification, "notif_1", text="\u0412\u0430\u0441 \u0434\u043e\u0431\u0430\u0432\u0438\u043b\u0438 \u043d\u0430 \u0434\u043e\u0441\u043a\u0443.", id_user=ids["user_3"], id_board=ids["board_1"])
    add(db, Notification, "notif_2", text="\u041d\u043e\u0432\u0430\u044f \u0438\u0434\u0435\u044f \u043e\u0436\u0438\u0434\u0430\u0435\u0442 \u043c\u043e\u0434\u0435\u0440\u0430\u0446\u0438\u0438.", id_user=ids["user_2"], id_board=ids["board_1"])

    add(db, EmailCode, "email_code_1", email="dasha@example.com", code="123456", expires_at=now + timedelta(minutes=10), is_used=False)
    add(db, EmailCode, "email_code_2", email="masha@example.com", code="654321", expires_at=now - timedelta(minutes=10), is_used=True)

    add(db, TgCode, "tg_code_1", id_user=ids["user_1"], code="111111", expires_at=now + timedelta(minutes=10), is_used=False)
    add(db, TgCode, "tg_code_2", id_user=ids["user_2"], code="222222", expires_at=now - timedelta(minutes=10), is_used=True)

    db.flush()


def seed_db():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        clear_seed_data(db)
        seed_dicts(db)
        seed_users(db)
        seed_boards(db)
        seed_ideas(db)
        seed_votings(db)
        seed_messages(db)
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_db()
    print("loaded")
