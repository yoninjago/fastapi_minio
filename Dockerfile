FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY ./fastapi_minio ./fastapi_minio

CMD ["uvicorn", "fastapi_minio.app:app", "--host", "0.0.0.0", "--port", "80"]