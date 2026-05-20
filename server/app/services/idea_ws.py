from uuid import UUID

from fastapi import WebSocket


class IdeasWsManager:
    def __init__(self) -> None:
        self.active: dict[UUID, list[WebSocket]] = {}

    async def connect(self, *, board_id: UUID, ws: WebSocket) -> None:
        await ws.accept()
        self.active.setdefault(board_id, []).append(ws)

    def disconnect(self, *, board_id: UUID, ws: WebSocket) -> None:
        sockets = self.active.get(board_id, [])
        if ws in sockets:
            sockets.remove(ws)
        if not sockets and board_id in self.active:
            del self.active[board_id]

    async def broadcast(self, *, board_id: UUID, data: dict) -> None:
        dead = []

        for ws in self.active.get(board_id, []):
            try:
                await ws.send_json(data)
            except RuntimeError:
                dead.append(ws)

        for ws in dead:
            self.disconnect(board_id=board_id, ws=ws)


ideas_ws = IdeasWsManager()
