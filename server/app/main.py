from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, boards, health, ideas, users, votings

app  = FastAPI(title="idk.app API", version="0.1.0")

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://127.0.0.1:63343",
    "http://localhost:63343",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(boards.router)
app.include_router(ideas.router)
app.include_router(votings.router)
