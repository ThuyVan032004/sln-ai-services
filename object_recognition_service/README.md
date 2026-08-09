# Object Recognition Service

Service nhận diện đối tượng xây dựng bằng FastAPI, sử dụng YOLO (ultralytics) và MLflow/DagsHub cho model registry.

## 1. Cấu hình biến môi trường

Service đọc cấu hình từ file `.env` tại thư mục gốc của service. Tạo/kiểm tra file `object_recognition_service/.env` với các biến sau:

```env
APPLICATION_NAME=object_recognition_service
DATABASE_URL=sqlite+aiosqlite:///object_recognition_service/app.db

DAGSHUB_OWNER=<dagshub-owner>
DAGSHUB_USERNAME=<dagshub-username>
DAGSHUB_REPO=<dagshub-repo>
DAGSHUB_TOKEN=<dagshub-token>

OBJECT_DETECTION_MODEL_NAME=<model-name>
OBJECT_DETECTION_MODEL_STAGE=Production
OBJECT_RECOGNITION_MODEL_STAGE=Production
```

## 2. Chạy service

### Cách 1: chạy bằng Docker Compose

Repo có file [docker-compose.yml](../docker-compose.yml) ở thư mục gốc, build từ [Dockerfile](Dockerfile) và giới hạn sẵn CPU/memory (1 CPU, 1GB RAM) cho container.

Chạy từ thư mục gốc repo (`sln-ai-services/`):

```bash
docker compose up --build
```

Mặc định compose dùng biến môi trường từ `object_recognition_service/.env`. Sửa file này (hoặc trỏ `env_file` sang file khác) nếu cần đổi cấu hình.

Dừng service:

```bash
docker compose down
```

### Cách 2: chạy bằng Docker thuần

Service cũng có thể build trực tiếp bằng [Dockerfile](Dockerfile) (build từ thư mục gốc repo vì cần copy cả `shared/`), không qua compose:

```bash
docker build -f object_recognition_service/Dockerfile -t object-recognition-service .
docker run -p 8786:8786 --cpus="1.0" --memory="1g" --env-file object_recognition_service/.env object-recognition-service
```
