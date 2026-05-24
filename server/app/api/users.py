import uuid
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, Query, UploadFile, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.models import User
from app.db.session import get_db
from app.schemas.users import UsernameCheckResponse, UserMeResponse, UserMeUpdateRequest
from app.services.users import UsersService

router = APIRouter(prefix="/api/v1/users", tags=["Users"])
UPLOAD_DIR = Path(__file__).resolve().parents[2] / "uploads" / "avatars"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def delete_avatar_file(photo_url: str | None) -> None:
    if not photo_url or not photo_url.startswith("/uploads/avatars/"):
        return

    path = (UPLOAD_DIR / Path(photo_url).name).resolve()
    if path.parent != UPLOAD_DIR.resolve():
        return

    path.unlink(missing_ok=True)


@router.get("/check-username", response_model=UsernameCheckResponse)
def check_username(username: str = Query(..., min_length=3, max_length=50), db: Session = Depends(get_db)):
    available = UsersService(db).check_username(username=username)
    if not available:
        return UsernameCheckResponse(available=False, message="Username уже занят")
    return UsernameCheckResponse(available=True, message="Username доступен")


@router.post("/avatar")
async def upload_avatar(file: UploadFile = File(...)):
    if file.content_type not in {"image/jpeg", "image/png", "image/webp"}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Можно загрузить только картинку")

    data = await file.read()
    if len(data) > 700_000:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Фото слишком большое")

    ext = ".jpg" if file.content_type == "image/jpeg" else ".png" if file.content_type == "image/png" else ".webp"
    name = f"{uuid.uuid4()}{ext}"
    (UPLOAD_DIR / name).write_bytes(data)
    return {"photo_url": f"/uploads/avatars/{name}"}


@router.get("/me", response_model=UserMeResponse)
def get_me(cur: User = Depends(get_current_user)):
    return UserMeResponse.model_validate(cur)


@router.patch("/me", response_model=UserMeResponse)
def update_me(
    body: UserMeUpdateRequest,
    background_tasks: BackgroundTasks,
    cur: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    old_photo_url = cur.photo_url

    try:
        user = UsersService(db).update_me(current_user=cur, username=body.username, name=body.name, photo_url=body.photo_url)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if old_photo_url and body.photo_url and old_photo_url != body.photo_url:
        background_tasks.add_task(delete_avatar_file, old_photo_url)

    return UserMeResponse.model_validate(user)
