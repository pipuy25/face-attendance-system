# Tổng quan và định hướng sản phẩm

## 1. Giới thiệu

Hệ thống chấm công bằng nhận diện khuôn mặt cho doanh nghiệp nhỏ. Nhân viên đứng trước camera để check-in/check-out. Quản trị viên theo dõi chất lượng nhận diện (tỷ lệ nhận sai) và nhận cảnh báo khi chất lượng giảm.

Đây là đồ án MLOps dùng model có sẵn (đề tài 9). Nhóm không huấn luyện model từ đầu mà tập trung vào vận hành: triển khai, giám sát, cảnh báo, CI/CD.

## 2. Bài toán và mục tiêu

**Vấn đề:** chấm công thủ công hoặc bằng thẻ dễ bị chấm hộ, tốn thời gian, khó kiểm tra lại.

**Mục tiêu:**
- Chấm công tự động bằng khuôn mặt, mỗi lần nhận diện dưới [2] giây.
- Ghi lại mọi lần nhận diện để kiểm tra và đối soát.
- Đo được tỷ lệ nhận sai theo thời gian và cảnh báo khi vượt ngưỡng.
- Chạy toàn hệ thống bằng một lệnh `docker compose up`.

**Đối tượng dùng:**

| Vai trò | Việc chính |
|---|---|
| Nhân viên | Đứng trước camera để chấm công |
| Quản trị viên | Đăng ký nhân viên, xem lịch sử, xác nhận hoặc sửa kết quả sai, xem dashboard |

## 3. Luồng hoạt động chính

1. **Đăng ký:** admin chụp 3-5 ảnh khuôn mặt của nhân viên. Hệ thống trích embedding và lưu vào vector DB.
2. **Chấm công:** camera chụp khung hình, hệ thống phát hiện mặt, trích embedding, tìm láng giềng gần nhất trong vector DB. Nếu độ tương đồng vượt ngưỡng thì ghi nhận check-in hoặc check-out.
3. **Giám sát:** hệ thống ghi log từng lần nhận diện (điểm tương đồng, kết quả, thời gian). Admin xác nhận hoặc sửa các trường hợp sai, tạo ra "nhãn đúng". Dashboard dùng các nhãn này để tính tỷ lệ nhận sai.

## 4. Kiến trúc dự kiến

| Thành phần | Công nghệ | Vai trò |
|---|---|---|
| Model nhận diện | InsightFace (ArcFace) | Phát hiện mặt, trích embedding |
| Vector DB | Qdrant hoặc pgvector (chốt sau thử nghiệm) | Tìm khuôn mặt gần nhất |
| Backend | FastAPI | API đăng ký, chấm công, log, metrics |
| CSDL quan hệ | PostgreSQL | Nhân viên, bản ghi chấm công, nhãn xác nhận |
| Giao diện | [React hoặc Streamlit] | Đăng ký, chấm công, lịch sử, admin |
| Giám sát | Prometheus + Grafana | Thu metrics, dashboard, cảnh báo |
| Triển khai | Docker Compose, GitHub Actions | Chạy hệ thống, CI/CD |

Luồng dữ liệu: Camera -> Giao diện -> Backend -> InsightFace -> Vector DB -> Backend ghi PostgreSQL và xuất metrics -> Prometheus -> Grafana.

## 5. Điểm khó: giám sát tỷ lệ nhận sai

- **FAR** (False Accept Rate): nhận nhầm người lạ thành nhân viên.
- **FRR** (False Reject Rate): từ chối nhầm nhân viên thật.
- Metrics theo dõi: FAR, FRR, điểm tương đồng trung bình, số lần admin sửa kết quả.
- Cảnh báo Grafana khi vượt ngưỡng, ví dụ FRR > [5%] trong 1 giờ.
- Đối chiếu số liệu thực tế với đánh giá offline trên bộ dữ liệu kiểm thử.

## 6. Phạm vi

**Bắt buộc (MVP):** đăng ký, chấm công, lịch sử, dashboard giám sát và cảnh báo, Docker Compose, CI/CD cơ bản.

**Nếu còn thời gian:** chống giả mạo (liveness detection), xuất báo cáo Excel, nhiều camera.

**Ngoài phạm vi:** huấn luyện model từ đầu.

## 7. Đánh giá và số liệu

- Độ chính xác: TAR tại FAR cố định (0.1% và 1%) trên bộ dữ liệu công khai (ví dụ LFW) và bộ dữ liệu tự thu thập có sự đồng ý của thành viên.
- Hiệu năng: độ trễ nhận diện p50/p95, thông lượng.
- Giám sát: tỷ lệ cảnh báo đúng/sai.

## 8. Rủi ro và quyền riêng tư

| Rủi ro | Biện pháp |
|---|---|
| Dữ liệu khuôn mặt là dữ liệu sinh trắc học nhạy cảm | Chỉ dùng dữ liệu của người đã đồng ý; không đưa ảnh lên GitHub; ưu tiên lưu embedding thay vì ảnh gốc; tham khảo Nghị định 13/2023/NĐ-CP |
| Độ chính xác giảm khi thiếu sáng, đeo khẩu trang | Thu thập dữ liệu đa điều kiện, điều chỉnh ngưỡng |
| Chậm tiến độ do phụ thuộc giữa các mảng | Chốt API contract sớm, dùng dữ liệu giả cho frontend |

## 9. Cấu trúc repo

- `backend/`: API FastAPI
- `ml/`: nhận diện, đánh giá mô hình
- `frontend/`: giao diện web
- `infra/`: Prometheus, Grafana, cấu hình
- `docs/`: tài liệu, báo cáo
- `.github/`: workflow CI, CODEOWNERS, template

## 10. Phân công và mốc tiến độ

| Thành viên | Vai trò |
|---|---|
| [Hoàn] | DevOps / điều phối (nhóm trưởng) |
| [Tuấn] | ML Engineer |
| [Thắng] | Backend |
| [Duy] | Frontend / Giám sát |

| Giai đoạn | Nội dung |
|---|---|
| Tuần 1 | Hoàn thiện repo, Compose khung, chạy thử InsightFace, chốt API contract |
| Tuần 2-3 | Đăng ký và chấm công end-to-end, giao diện cơ bản |
| Tuần 4 | Prometheus/Grafana, cảnh báo, tính FAR/FRR |
| Tuần 5 | Đánh giá, tối ưu, kiểm thử |
| Tuần 6 | Hoàn thiện báo cáo, demo |