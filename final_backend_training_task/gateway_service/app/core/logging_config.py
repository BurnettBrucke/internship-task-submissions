import json
import logging
import sys
from datetime import datetime, timezone


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "service": getattr(record, "service", "gateway"),
            "event": getattr(record, "event", record.getMessage()),
            "request_id": getattr(record, "request_id", None),
            "correlation_id": getattr(record, "correlation_id", None),
            "job_id": getattr(record, "job_id", None),
            "duration_ms": getattr(record, "duration_ms", None),
            "status": getattr(record, "status", None),
        }

        return json.dumps(data)


def configure_logging() -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)
