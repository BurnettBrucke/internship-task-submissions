import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from fastapi.testclient import TestClient

from processing_service.app.main import app


client = TestClient(app)


def test_internal_auth_missing_token():
    response = client.get(
        "/internal/v1/jobs/non-existing-job"
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid internal service credential"


def test_internal_auth_invalid_token():
    response = client.get(
        "/internal/v1/jobs/non-existing-job",
        headers={
            "Authorization": "Bearer wrong-token"
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid internal service credential"


def test_internal_auth_valid_token():
    response = client.get(
        "/internal/v1/jobs/non-existing-job",
        headers={
            "Authorization": "Bearer day8-internal-secret"
        },
    )

    # Authentication passes, then endpoint checks whether job exists.
    assert response.status_code == 404
    assert response.json()["detail"] == "Job not found"