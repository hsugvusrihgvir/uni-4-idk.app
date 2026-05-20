from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.db.models import User
from app.schemas.boards import (
    BoardCreateRequest,
    BoardCreateResponse,
    BoardDetailResponse,
    BoardItemResponse,
    BoardMemberCreateRequest,
    BoardMemberResponse,
    BoardMemberRoleRequest,
    BoardMembersListResponse,
    BoardUpdateRequest,
    BoardsListResponse,
)
from app.schemas.ideas import IdeaItemResponse, IdeaResponse, IdeasListResponse
from app.services.boards import BoardsService
from app.services.ideas import IdeasService

router = APIRouter(prefix="/api/v1/boards", tags=["Boards"])


def member_response(member):
    return BoardMemberResponse(
        id=member.user.id,
        username=member.user.username,
        name=member.user.name,
        photo_url=member.user.photo_url,
        role=member.role,
    )


@router.post("", response_model=BoardCreateResponse)
def create_board(
    body: BoardCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    board = BoardsService(db).create(
        current_user=current_user,
        title=body.title,
        description=body.description,
        moderation=body.moderation,
        anon_ideas=body.anon_ideas,
    )

    return BoardCreateResponse.model_validate(board)


@router.get("", response_model=BoardsListResponse)
def get_boards(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    members = BoardsService(db).get_my_boards(current_user=current_user)

    return BoardsListResponse(
        items=[
            BoardItemResponse(
                id=member.board.id,
                title=member.board.title,
                description=member.board.description,
                role=member.role,
            )
            for member in members
        ]
    )


@router.get("/{board_id}", response_model=BoardDetailResponse)
def get_board(
    board_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        member = BoardsService(db).get_board(
            current_user=current_user,
            board_id=board_id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    board = member.board

    return BoardDetailResponse(
        id=board.id,
        title=board.title,
        description=board.description,
        role=member.role,
        anon_ideas=board.anon_ideas,
        moderation=board.moderation,
        created_at=board.created_at,
        ideas=[
            IdeaItemResponse.model_validate(idea)
            for idea in board.ideas
        ],
    )


@router.patch("/{board_id}", response_model=BoardCreateResponse)
def update_board(
    board_id: UUID,
    body: BoardUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        board = BoardsService(db).update(
            current_user=current_user,
            board_id=board_id,
            title=body.title,
            description=body.description,
            moderation=body.moderation,
            anon_ideas=body.anon_ideas,
        )
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

    return BoardCreateResponse.model_validate(board)


@router.delete("/{board_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_board(
    board_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        BoardsService(db).delete(current_user=current_user, board_id=board_id)
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


@router.get("/{board_id}/members", response_model=BoardMembersListResponse)
def get_board_members(
    board_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        members = BoardsService(db).get_members(current_user=current_user, board_id=board_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    return BoardMembersListResponse(items=[member_response(member) for member in members])


@router.post("/{board_id}/members", response_model=BoardMemberResponse)
def add_board_member(
    board_id: UUID,
    body: BoardMemberCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        member = BoardsService(db).add_member(
            current_user=current_user,
            board_id=board_id,
            username=body.username,
            role=body.role,
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return member_response(member)


@router.patch("/{board_id}/members/{user_id}/role", response_model=BoardMemberResponse)
def change_board_member_role(
    board_id: UUID,
    user_id: UUID,
    body: BoardMemberRoleRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        member = BoardsService(db).change_member_role(
            current_user=current_user,
            board_id=board_id,
            user_id=user_id,
            role=body.role,
        )
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return member_response(member)


@router.delete("/{board_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_board_member(
    board_id: UUID,
    user_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        BoardsService(db).delete_member(current_user=current_user, board_id=board_id, user_id=user_id)
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/{board_id}/ideas/moderation", response_model=IdeasListResponse)
def get_moderation_ideas(
    board_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        ideas = IdeasService(db).get_moderation(current_user=current_user, board_id=board_id)
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    return IdeasListResponse(items=[IdeaResponse.model_validate(idea) for idea in ideas])


@router.get("/{board_id}/ideas", response_model=IdeasListResponse)
def get_board_ideas(
    board_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        ideas = IdeasService(db).get_by_board(
            current_user=current_user,
            board_id=board_id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    return IdeasListResponse(
        items=[
            IdeaResponse.model_validate(idea)
            for idea in ideas
        ]
    )
