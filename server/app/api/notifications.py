from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.models import User
from app.db.session import get_db
from app.schemas.notifications import NotificationResponse, NotificationsListResponse
from app.services.notifications import NotificationsService

router = APIRouter(prefix="/api/v1/notifications", tags=["Notifications"])


@router.get("", response_model=NotificationsListResponse)
def get_notifications(cur: User = Depends(get_current_user), db: Session = Depends(get_db)):
    notifs = NotificationsService(db).get_my(current_user=cur)
    return NotificationsListResponse(items=[NotificationResponse.model_validate(n) for n in notifs])


@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notification(notification_id: UUID, cur: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        NotificationsService(db).delete(current_user=cur, notification_id=notification_id)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
