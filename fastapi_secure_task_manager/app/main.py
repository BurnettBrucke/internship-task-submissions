from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.tasks import router as tasks_router
app = FastAPI(
    title="Secure Task Manager API",
    description="FastAPI Task Management API with Authentication and Security",
    version="1.0.0",
)

app.include_router(auth_router)
app.include_router(tasks_router)

@app.get("/health")
def health_check():
    return {
        "status":"healthy"
    }

