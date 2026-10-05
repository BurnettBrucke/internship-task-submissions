from fastapi import FastAPI

from app.api.internal.jobs import router as jobs_router


app = FastAPI(
    title="Day 8 Processing Service",
    version="1.0.0",
)


app.include_router(jobs_router)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "processing",
    }