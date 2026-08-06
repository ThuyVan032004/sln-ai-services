# Object Recognition Service

Service nhận diện đối tượng xây dựng bằng FastAPI, sử dụng YOLO (ultralytics) và MLflow/DagsHub cho model registry.

## Yêu cầu

- Python >= 3.12 (xem [.python-version](.python-version))
- [uv](https://docs.astral.sh/uv/) đã cài đặt

Cài `uv` nếu chưa có:

```powershell
# Windows (PowerShell)
irm https://astral.sh/uv/install.ps1 | iex
```

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Cấu trúc thư mục liên quan

Service này phụ thuộc vào package nội bộ `shared` nằm cùng cấp (`../shared`), được khai báo trong [pyproject.toml](pyproject.toml):

```toml
[tool.uv.sources]
shared = { path = "../shared", editable = true }
```

Vì vậy cần giữ nguyên cấu trúc repo:

```
sln-ai-services/
├── object_recognition_service/
└── shared/
```

## 1. Cài đặt dependencies

Chạy trong thư mục `object_recognition_service/`:

```bash
cd object_recognition_service
uv sync
```

## 2. Cấu hình biến môi trường

Service đọc cấu hình từ file `.env` tại thư mục gốc của service. Tạo/kiểm tra file `object_recognition_service/.env` với các biến sau:

```env
APPLICATION_NAME=object_recognition_service
DATABASE_URL=postgresql+asyncpg://<user>:<password>@<host>/<database>

AWS_S3_BUCKET=<s3-bucket-name>
AWS_ACCESS_KEY_ID=<aws-access-key-id>
AWS_SECRET_ACCESS_KEY=<aws-secret-access-key>
AWS_REGION=<aws-region>

DAGSHUB_OWNER=<dagshub-owner>
DAGSHUB_USERNAME=<dagshub-username>
DAGSHUB_REPO=<dagshub-repo>
DAGSHUB_TOKEN=<dagshub-token>

OBJECT_DETECTION_MODEL_NAME=<model-name>
OBJECT_DETECTION_MODEL_STAGE=Production
OBJECT_RECOGNITION_MODEL_STAGE=Production
```

> Không commit file `.env` chứa credential thật lên git.

## 3. Migrate database (Alembic)

Cấu hình Alembic nằm ở [alembic.ini](alembic.ini) (script location: `migrator/`). Cập nhật `sqlalchemy.url` trong `alembic.ini` hoặc qua biến môi trường tương ứng trước khi chạy.

```bash
# Áp dụng toàn bộ migration mới nhất
uv run alembic upgrade head
```

## 4. Chạy service

### Cách 1: dùng uvicorn qua uv run (khuyến nghị)

```bash
uvicorn object_recognition_service.host.main:app --env-file object_recognition_service/.env --reload
```

Chạy lệnh này từ thư mục gốc repo (`sln-ai-services/`), vì module path là `object_recognition_service.host.main`.

Sau khi chạy, service sẽ lắng nghe tại `http://localhost:8000`.

- Health check: `GET http://localhost:8000/`
- API docs (Swagger UI): `http://localhost:8000/docs`

### Cách 2: chạy bằng Docker Compose (khuyến nghị)

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

### Cách 3: chạy bằng Docker thuần (tham khảo)

Service cũng có thể build trực tiếp bằng [Dockerfile](Dockerfile) (build từ thư mục gốc repo vì cần copy cả `shared/`), không qua compose:

```bash
docker build -f object_recognition_service/Dockerfile -t object-recognition-service .
docker run -p 8000:8000 --cpus="1.0" --memory="1g" --env-file object_recognition_service/.env object-recognition-service
```
