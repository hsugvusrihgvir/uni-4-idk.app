from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.db.models import User
from app.schemas.users import (
    UsernameCheckResponse,
    UserMeResponse,
    UserMeUpdateRequest,
)
from app.services.users import UsersService

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.get("/check-username", response_model=UsernameCheckResponse)
def check_username(
    username: str = Query(..., min_length=3, max_length=50),
    db: Session = Depends(get_db),
):
    available = UsersService(db).check_username(username=username)

    if not available:
        return UsernameCheckResponse(
            available=False,
            message="Username уже занят",
        )

    return UsernameCheckResponse(
        available=True,
        message="Username доступен",
    )


@router.get("/me", response_model=UserMeResponse)
def get_me(cur: User = Depends(get_current_user)):
    return UserMeResponse.model_validate(cur)


@router.patch("/me", response_model=UserMeResponse)
def update_me(
    body: UserMeUpdateRequest,
    cur: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        user = UsersService(db).update_me(current_user=cur, username=body.username, name=body.name, photo_url=body.photo_url)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return UserMeResponse.model_validate(user)
