FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY processing_service/app ./processing_service/app

EXPOSE 8001

CMD ["uvicorn", "processing_service.app.main:app", "--host", "0.0.0.0", "--port", "8001"]