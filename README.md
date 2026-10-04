# face-attendance-system
# Hệ thống chấm công bằng nhận diện khuôn mặt

Đồ án MLOps với model có sẵn (đề tài 9). Hệ thống nhận diện khuôn mặt nhân viên để chấm công, kèm giám sát tỷ lệ nhận sai và cảnh báo khi vượt ngưỡng.

## Công nghệ dự kiến

- Model nhận diện: InsightFace
- Vector DB: Qdrant hoặc pgvector
- Backend: FastAPI, PostgreSQL
- Giám sát: Prometheus, Grafana
- Triển khai: Docker Compose, GitHub Actions

## Chạy thử backend

```bash
docker compose up --build
```
Mở http://localhost:8000/health, thấy `{"status": "ok"}` là chạy được.

## Cấu trúc thư mục

- `backend/`: API FastAPI
- `ml/`: nhận diện, đánh giá mô hình
- `frontend/`: giao diện web
- `infra/`: Prometheus, Grafana
- `docs/`: tài liệu, báo cáo

## Quy trình làm việc

- Không push trực tiếp vào `main`; tạo nhánh `feature/...` hoặc `docs/...` rồi mở Pull Request.
- PR phải qua CI (lint, test, docker-build) trước khi merge.
- Chi tiết định hướng sản phẩm: xem `docs/overview.md`.