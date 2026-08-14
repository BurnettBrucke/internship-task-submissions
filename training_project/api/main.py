from fastapi import FastAPI

app = FastAPI(
    title="Student Training Portal API",
    description="REST API for the Student Training Portal",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "Student Training Portal API is running"
    }