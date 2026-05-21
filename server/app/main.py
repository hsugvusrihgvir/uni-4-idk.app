from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api import auth, board_admin, boards, health, idea_ws, ideas, moderation, notifications, users, votings

app = FastAPI(title="idk.app API", version="0.1.0")
BASE_DIR = Path(__file__).resolve().parents[1]
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://127.0.0.1:63343",
    "http://localhost:63343",
]

# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(boards.router)
app.include_router(board_admin.router)
app.include_router(ideas.router)
app.include_router(idea_ws.router)
app.include_router(moderation.router)
app.include_router(notifications.router)
app.include_router(votings.router)
