from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.models import User
from app.db.session import get_db
from app.schemas.votings import (
    VoteCreateRequest,
    VoteResponse,
    VotingCreateRequest,
    VotingResponse,
    VotingResultsResponse,
    VotingsListResponse,
)
from app.services.voting_admin import VotingAdminService
from app.services.votings import VotingsService

router = APIRouter(tags=["Votings"])


def voting_response(voting):
    return VotingResponse(id=voting.id, board_id=voting.board_id, type=voting.voting_type.type, created_at=voting.created_at)


@router.post("/api/v1/boards/{board_id}/votings", response_model=VotingResponse)
def create_voting(
    board_id: UUID,
    body: VotingCreateRequest,
    cur: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        voting = VotingAdminService(db).create(cur=cur, board_id=board_id, type=body.type)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return voting_response(voting)


@router.get("/api/v1/boards/{board_id}/votings", response_model=VotingsListResponse)
def get_board_votings(board_id: UUID, cur: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        votings = VotingsService(db).get_by_board(current_user=cur, board_id=board_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return VotingsListResponse(items=[voting_response(v) for v in votings])


@router.delete("/api/v1/votings/{voting_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_voting(voting_id: UUID, cur: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        VotingAdminService(db).delete(cur=cur, voting_id=voting_id)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/api/v1/votes", response_model=VoteResponse)
def create_vote(body: VoteCreateRequest, cur: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        vote = VotingsService(db).vote(current_user=cur, voting_id=body.voting_id, idea_id=body.idea_id)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return VoteResponse.model_validate(vote)


@router.get("/api/v1/votings/{voting_id}/results", response_model=VotingResultsResponse)
def get_voting_results(voting_id: UUID, cur: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        items = VotingsService(db).get_results(current_user=cur, voting_id=voting_id)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return VotingResultsResponse(items=items)
