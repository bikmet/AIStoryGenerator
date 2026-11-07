from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings

app = FastAPI(
    title="Choose Your Own Adventure Game API",
    description="api to generate cool stories",
    version="1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS, #stated in config.py on what origins we can use (from .env file)
    allow_credentials=True,
    allow_methdos=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)