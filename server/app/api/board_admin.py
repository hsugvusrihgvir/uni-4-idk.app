from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.models import User
from app.db.session import get_db
from app.schemas.boards import (
    BoardCreateResponse,
    BoardMemberCreateRequest,
    BoardMemberResponse,
    BoardMemberRoleRequest,
    BoardMembersListResponse,
    BoardUpdateRequest,
)
from app.services.board_admin import BoardAdminService

router = APIRouter(prefix="/api/v1/boards", tags=["Board admin"])


def member_response(member):
    return BoardMemberResponse(
        id=member.user.id,
        username=member.user.username,
        name=member.user.name,
        photo_url=member.user.photo_url,
        role=member.role,
    )


@router.patch("/{board_id}", response_model=BoardCreateResponse)
def update_board(
    board_id: UUID,
    body: BoardUpdateRequest,
    cur: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        board = BoardAdminService(db).update(
            cur=cur,
            board_id=board_id,
            title=body.title,
            description=body.description,
            moderation=body.moderation,
            anon_ideas=body.anon_ideas,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

    return BoardCreateResponse.model_validate(board)


@router.delete("/{board_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_board(
    board_id: UUID,
    cur: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        BoardAdminService(db).delete_board(cur=cur, board_id=board_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.get("/{board_id}/members", response_model=BoardMembersListResponse)
def get_board_members(
    board_id: UUID,
    cur: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        members = BoardAdminService(db).members(cur=cur, board_id=board_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return BoardMembersListResponse(items=[member_response(member) for member in members])


@router.post("/{board_id}/members", response_model=BoardMemberResponse)
def add_board_member(
    board_id: UUID,
    body: BoardMemberCreateRequest,
    cur: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        member = BoardAdminService(db).add_member(cur=cur, board_id=board_id, username=body.username, role=body.role)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return member_response(member)


@router.patch("/{board_id}/members/{user_id}/role", response_model=BoardMemberResponse)
def change_board_member_role(
    board_id: UUID,
    user_id: UUID,
    body: BoardMemberRoleRequest,
    cur: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        member = BoardAdminService(db).change_role(cur=cur, board_id=board_id, user_id=user_id, role=body.role)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return member_response(member)


@router.delete("/{board_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_board_member(
    board_id: UUID,
    user_id: UUID,
    cur: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        BoardAdminService(db).delete_member(cur=cur, board_id=board_id, user_id=user_id)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
