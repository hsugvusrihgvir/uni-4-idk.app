from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.db.models import User
from app.schemas.ideas import IdeaCreateRequest, IdeaResponse
from app.services.ideas import IdeasService

router = APIRouter(prefix="/api/v1/ideas", tags=["Ideas"])


@router.post("", response_model=IdeaResponse)
def create_idea(
    body: IdeaCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        idea = IdeasService(db).create(
            current_user=current_user,
            board_id=body.board_id,
            title=body.title,
            description=body.description,
            is_anonymous=body.is_anonymous,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return IdeaResponse.model_validate(idea)


@router.delete("/{idea_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_idea(
    idea_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        IdeasService(db).delete(current_user=current_user, idea_id=idea_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )
