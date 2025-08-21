from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import api_router

app = FastAPI(
    title="api",
    # generate_unique_id_function=custom_generate_unique_id,
)

origins = [
    "http://localhost:5173",
    "http://0.0.0.0:5173",
    "https://schedule-phi.vercel.app",  # Your Vercel front-end URL
    "https://schedule-git-main-shareer28.vercel.app"  # Alternative Vercel URL format
]

app.include_router(api_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
