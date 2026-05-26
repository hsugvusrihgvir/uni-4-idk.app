from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.auth import (
    AuthLoginRequest,
    AuthLoginResponse,
    AuthMessageResponse,
    AuthRefreshRequest,
    AuthRefreshResponse,
    AuthRegisterRequest,
    AuthUserResponse,
    AuthVerifyRequest,
    AuthVerifyResponse,
)
from app.services.auth import AuthService

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Auth"],
)


@router.post("/login", response_model=AuthLoginResponse)
def login(body: AuthLoginRequest, db: Session = Depends(get_db)):
    try:
        exists = AuthService(db).login(email=body.email)
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

    if not exists:
        return AuthLoginResponse(
            exists=False,
            message="Аккаунт не найден",
        )

    return AuthLoginResponse(
        exists=True,
        message="Код отправлен на email",
    )


@router.post("/register", response_model=AuthMessageResponse)
def register(body: AuthRegisterRequest, db: Session = Depends(get_db)):
    try:
        AuthService(db).register(
            email=body.email,
            username=body.username,
            name=body.name,
            photo_url=body.photo_url,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

    return AuthMessageResponse(message="Код отправлен на email")


@router.post("/verify", response_model=AuthVerifyResponse)
def verify(body: AuthVerifyRequest, db: Session = Depends(get_db)):
    try:
        access, refresh, user = AuthService(db).verify(
            email=body.email,
            code=body.code,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return AuthVerifyResponse(
        access_token=access,
        refresh_token=refresh,
        user=AuthUserResponse.model_validate(user),
    )


@router.post("/refresh", response_model=AuthRefreshResponse)
def refresh(body: AuthRefreshRequest, db: Session = Depends(get_db)):
    try:
        access = AuthService(db).refresh(refresh_token=body.refresh_token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )

    return AuthRefreshResponse(access_token=access)
