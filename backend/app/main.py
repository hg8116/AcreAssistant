from fastapi import FastAPI

app = FastAPI(
    title="AcreAssistant API",
    description="AI real-estate sales assistant for Northstar Homes",
    version="0.1.0",
)


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
