from fastapi import APIRouter, Depends, HTTPException, status
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
            board_id=body.id_board,
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
