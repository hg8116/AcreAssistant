from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.api.sessions import router as sessions_router


app = FastAPI(
    title="AcreAssistant API",
    description="AI real-estate sales assistant for Northstar Homes",
    version="0.1.0",
)


app.include_router(sessions_router)
app.include_router(chat_router)


@app.get("/")
async def root():
    return {
        "message": "AcreAssistant API is running"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }
