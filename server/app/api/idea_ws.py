from uuid import UUID

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status
from jose import JWTError

from app.core.security import validate_access_token
from app.db.queries.boards import BoardsQueries
from app.db.queries.users import UsersQueries
from app.db.session import SessionLocal
from app.services.idea_ws import ideas_ws

router = APIRouter(tags=["Ideas websocket"])


@router.websocket("/api/v1/boards/{board_id}/ideas/ws")
async def board_ideas_ws(ws: WebSocket, board_id: UUID, token: str | None = None):
    db = SessionLocal()

    try:
        if not token:
            await ws.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        try:
            user_id = UUID(validate_access_token(token))
        except (JWTError, ValueError):
            await ws.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        user = UsersQueries(db).get_by_id(user_id)
        member = BoardsQueries(db).get_member(board_id=board_id, user_id=user_id)

        if user is None or member is None:
            await ws.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        await ideas_ws.connect(board_id=board_id, ws=ws)

        try:
            while True:
                await ws.receive_text()
        except WebSocketDisconnect:
            ideas_ws.disconnect(board_id=board_id, ws=ws)
    finally:
        db.close()
