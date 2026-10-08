import json
import logging
from datetime import datetime, timezone


logger = logging.getLogger("gateway-service")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()

formatter = logging.Formatter("%(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)


def log_event(
    event: str,
    level: str = "INFO",
    request_id: str | None = None,
    correlation_id: str | None = None,
    job_id: str | None = None,
    duration_ms: float | None = None,
    status: str | None = None,
):
    log_data = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "level": level,
        "service": "gateway-service",
        "event": event,
        "request_id": request_id,
        "correlation_id": correlation_id,
        "job_id": job_id,
        "duration_ms": duration_ms,
        "status": status,
    }

    logger.info(json.dumps(log_data))