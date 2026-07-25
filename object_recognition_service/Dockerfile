FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY shared /app/shared
COPY object_recognition_service /app/object_recognition_service

RUN pip install --upgrade pip \
    && pip install -e /app/shared \
    && pip install -e /app/object_recognition_service \
    && pip uninstall -y opencv-python opencv-python-headless \
    && pip install --no-cache-dir opencv-python-headless

EXPOSE 8000

CMD ["uvicorn", "object_recognition_service.host.main:app", "--host", "0.0.0.0", "--port", "8000"]