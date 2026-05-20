from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db.models import Idea, Vote, Voting, VotingType


class VotingsQueries:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_or_create_type(self, *, type: str) -> VotingType:
        stmt = select(VotingType).where(VotingType.type == type).limit(1)
        t = self.db.execute(stmt).scalar_one_or_none()

        if t is not None:
            return t

        t = VotingType(type=type)

        self.db.add(t)
        self.db.flush()

        return t

    def create(self, *, board_id: UUID, type: str) -> Voting:
        t = self.get_or_create_type(type=type)
        voting = Voting(board_id=board_id, type_id=t.id, voting_type=t)

        self.db.add(voting)
        self.db.flush()

        return voting

    def get_by_id(self, *, voting_id: UUID) -> Voting | None:
        stmt = (
            select(Voting)
            .options(selectinload(Voting.voting_type))
            .where(Voting.id == voting_id)
            .limit(1)
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def get_by_board(self, *, board_id: UUID) -> list[Voting]:
        stmt = (
            select(Voting)
            .options(selectinload(Voting.voting_type))
            .where(Voting.board_id == board_id)
            .order_by(Voting.created_at.desc())
        )
        return list(self.db.execute(stmt).scalars().all())

    def delete(self, voting: Voting) -> None:
        self.db.delete(voting)
        self.db.flush()

    def get_vote(self, *, user_id: UUID, voting_id: UUID, idea_id: UUID) -> Vote | None:
        stmt = (
            select(Vote)
            .where(
                Vote.user_id == user_id,
                Vote.voting_id == voting_id,
                Vote.idea_id == idea_id,
            )
            .limit(1)
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def create_vote(self, *, user_id: UUID, voting_id: UUID, idea_id: UUID) -> Vote:
        vote = Vote(user_id=user_id, voting_id=voting_id, idea_id=idea_id)

        self.db.add(vote)
        self.db.flush()

        return vote

    def get_votes(self, *, voting_id: UUID) -> list[Vote]:
        stmt = (
            select(Vote)
            .options(selectinload(Vote.idea).selectinload(Idea.idea_status))
            .where(Vote.voting_id == voting_id)
        )
        return list(self.db.execute(stmt).scalars().all())
