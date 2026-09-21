from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.api.chat import router as chat_router
from app.api.sessions import router as sessions_router
from app.api.bookings import router as bookings_router


app = FastAPI(
    title="AcreAssistant API",
    description="AI real-estate sales assistant for Northstar Homes",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sessions_router)
app.include_router(chat_router)
app.include_router(bookings_router)

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
