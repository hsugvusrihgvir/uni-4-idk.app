from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.models import User
from app.db.session import get_db
from app.schemas.ideas import IdeaResponse, IdeasListResponse, IdeaStatusUpdateRequest
from app.services.moderation import ModerationService

router = APIRouter(tags=["Moderation"])


@router.get("/api/v1/boards/{board_id}/ideas/moderation", response_model=IdeasListResponse)
def get_moderation_ideas(
    board_id: UUID,
    cur: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        ideas = ModerationService(db).pending(cur=cur, board_id=board_id)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return IdeasListResponse(items=[IdeaResponse.model_validate(idea) for idea in ideas])


@router.patch("/api/v1/ideas/{idea_id}/status", response_model=IdeaResponse)
def update_idea_status(
    idea_id: UUID,
    body: IdeaStatusUpdateRequest,
    cur: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        idea = ModerationService(db).set_status(cur=cur, idea_id=idea_id, status=body.status)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return IdeaResponse.model_validate(idea)
