FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY gateway_service/app ./gateway_service/app

EXPOSE 8000

CMD ["uvicorn", "gateway_service.app.main:app", "--host", "0.0.0.0", "--port", "8000"]