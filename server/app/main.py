from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app  = FastAPI(title="idk.app", version="0.1.0")

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
