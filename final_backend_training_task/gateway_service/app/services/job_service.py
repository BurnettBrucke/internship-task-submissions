from app.clients.processing_client import ProcessingClient
from app.schemas.job import JobCreate

processing_client = ProcessingClient()


async def create_job(
    payload: JobCreate,
):
    return await processing_client.create_job(payload)


async def get_job(
    job_id: int,
):
    return await processing_client.get_job(job_id)
