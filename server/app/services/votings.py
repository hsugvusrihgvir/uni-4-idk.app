from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models import User, Vote, Voting
from app.db.queries.boards import BoardsQueries
from app.db.queries.ideas import IdeasQueries
from app.db.queries.votings import VotingsQueries


ALLOWED_TYPES = {"like", "yes_no"}


class VotingsService:
    def __init__(self, db: Session) -> None:
        self.q_b = BoardsQueries(db)
        self.q_i = IdeasQueries(db)
        self.q_v = VotingsQueries(db)

    def get_by_board(self, *, current_user: User, board_id: UUID) -> list[Voting]:
        member = self.q_b.get_member(board_id=board_id, user_id=current_user.id)

        if member is None:
            raise ValueError("Board not found")

        return self.q_v.get_by_board(board_id=board_id)

    def vote(self, *, current_user: User, voting_id: UUID, idea_id: UUID) -> Vote:
        voting = self.q_v.get_by_id(voting_id=voting_id)

        if voting is None:
            raise ValueError("Voting not found")

        member = self.q_b.get_member(board_id=voting.board_id, user_id=current_user.id)

        if member is None:
            raise PermissionError("Only board member can vote")

        idea = self.q_i.get_by_id(idea_id=idea_id)

        if idea is None:
            raise ValueError("Idea not found")

        if idea.board_id != voting.board_id:
            raise ValueError("Idea does not belong to voting board")

        if idea.status != "approved":
            raise ValueError("Only approved idea can be voted")

        vote = self.q_v.get_vote(user_id=current_user.id, voting_id=voting_id, idea_id=idea_id)

        if vote is not None:
            raise ValueError("Vote already exists")

        if voting.voting_type.type == "yes_no":
            for old_vote in self.q_v.get_user_votes(user_id=current_user.id, voting_id=voting_id):
                self.q_v.delete_vote(old_vote)

        return self.q_v.create_vote(user_id=current_user.id, voting_id=voting_id, idea_id=idea_id)

    def delete_vote(self, *, current_user: User, voting_id: UUID, idea_id: UUID) -> None:
        voting = self.q_v.get_by_id(voting_id=voting_id)

        if voting is None:
            raise ValueError("Voting not found")

        member = self.q_b.get_member(board_id=voting.board_id, user_id=current_user.id)

        if member is None:
            raise PermissionError("Only board member can vote")

        vote = self.q_v.get_vote(user_id=current_user.id, voting_id=voting_id, idea_id=idea_id)

        if vote is None:
            raise ValueError("Vote not found")

        self.q_v.delete_vote(vote)

    def get_results(self, *, current_user: User, voting_id: UUID) -> list[dict]:
        voting = self.q_v.get_by_id(voting_id=voting_id)

        if voting is None:
            raise ValueError("Voting not found")

        member = self.q_b.get_member(board_id=voting.board_id, user_id=current_user.id)

        if member is None:
            raise PermissionError("Only board member can view results")

        ideas = self.q_i.get_by_board_and_status(board_id=voting.board_id, status="approved")
        votes = self.q_v.get_votes(voting_id=voting_id)
        user_vote_ids = {vote.idea_id for vote in votes if vote.user_id == current_user.id}
        total = len(votes)
        result = {
            idea.id: {
                "idea_id": idea.id,
                "title": idea.title,
                "votes_count": 0,
                "approval_percent": 0,
                "user_voted": idea.id in user_vote_ids,
            }
            for idea in ideas
        }

        for vote in votes:
            if vote.idea_id not in result:
                result[vote.idea_id] = {
                    "idea_id": vote.idea_id,
                    "title": vote.idea.title,
                    "votes_count": 0,
                    "approval_percent": 0,
                    "user_voted": vote.idea_id in user_vote_ids,
                }

            result[vote.idea_id]["votes_count"] += 1
            result[vote.idea_id]["user_voted"] = vote.idea_id in user_vote_ids

        for item in result.values():
            item["approval_percent"] = round(item["votes_count"] / total * 100) if total else 0

        return sorted(result.values(), key=lambda item: item["votes_count"], reverse=True)
