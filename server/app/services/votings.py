from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models import User, Vote, Voting
from app.db.queries.boards import BoardsQueries
from app.db.queries.ideas import IdeasQueries
from app.db.queries.votings import VotingsQueries


ALLOWED_TYPES = {"like", "yes_no"}


class VotingsService:
    def __init__(self, db: Session) -> None:
        self.q_boards = BoardsQueries(db)
        self.q_ideas = IdeasQueries(db)
        self.q_votings = VotingsQueries(db)

    def create(self, *, current_user: User, board_id: UUID, type: str) -> Voting:
        member = self.q_boards.get_member(board_id=board_id, user_id=current_user.id)

        if member is None:
            raise ValueError("Board not found")

        if member.role != "admin":
            raise PermissionError("Only admin can create voting")

        if type not in ALLOWED_TYPES:
            raise ValueError("Invalid voting type")

        return self.q_votings.create(board_id=board_id, type=type)

    def get_by_board(self, *, current_user: User, board_id: UUID) -> list[Voting]:
        member = self.q_boards.get_member(board_id=board_id, user_id=current_user.id)

        if member is None:
            raise ValueError("Board not found")

        return self.q_votings.get_by_board(board_id=board_id)

    def delete(self, *, current_user: User, voting_id: UUID) -> None:
        voting = self.q_votings.get_by_id(voting_id=voting_id)

        if voting is None:
            raise ValueError("Voting not found")

        member = self.q_boards.get_member(board_id=voting.board_id, user_id=current_user.id)

        if member is None:
            raise ValueError("Board not found")

        if member.role != "admin":
            raise PermissionError("Only admin can delete voting")

        self.q_votings.delete(voting)

    def vote(self, *, current_user: User, voting_id: UUID, idea_id: UUID) -> Vote:
        voting = self.q_votings.get_by_id(voting_id=voting_id)

        if voting is None:
            raise ValueError("Voting not found")

        member = self.q_boards.get_member(board_id=voting.board_id, user_id=current_user.id)

        if member is None:
            raise PermissionError("Only board member can vote")

        idea = self.q_ideas.get_by_id(idea_id=idea_id)

        if idea is None:
            raise ValueError("Idea not found")

        if idea.board_id != voting.board_id:
            raise ValueError("Idea does not belong to voting board")

        if idea.status != "approved":
            raise ValueError("Only approved idea can be voted")

        vote = self.q_votings.get_vote(user_id=current_user.id, voting_id=voting_id, idea_id=idea_id)

        if vote is not None:
            raise ValueError("Vote already exists")

        return self.q_votings.create_vote(user_id=current_user.id, voting_id=voting_id, idea_id=idea_id)

    def get_results(self, *, current_user: User, voting_id: UUID) -> list[dict]:
        voting = self.q_votings.get_by_id(voting_id=voting_id)

        if voting is None:
            raise ValueError("Voting not found")

        member = self.q_boards.get_member(board_id=voting.board_id, user_id=current_user.id)

        if member is None:
            raise PermissionError("Only board member can view results")

        votes = self.q_votings.get_votes(voting_id=voting_id)
        total = len(votes)
        result = {}

        for vote in votes:
            if vote.idea_id not in result:
                result[vote.idea_id] = {
                    "idea_id": vote.idea_id,
                    "title": vote.idea.title,
                    "votes_count": 0,
                    "approval_percent": 0,
                }

            result[vote.idea_id]["votes_count"] += 1

        for item in result.values():
            item["approval_percent"] = round(item["votes_count"] / total * 100) if total else 0

        return sorted(result.values(), key=lambda item: item["votes_count"], reverse=True)
