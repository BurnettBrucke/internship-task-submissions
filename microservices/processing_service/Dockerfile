FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
COPY alembic.ini .

RUN pip install --no-cache-dir -r requirements.txt

COPY processing_service ./processing_service

EXPOSE 8001

CMD ["uvicorn", "processing_service.app.main:app", "--host", "0.0.0.0", "--port", "8001"]