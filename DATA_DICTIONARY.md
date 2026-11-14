# Data Dictionary — DUA Edu Survey

## 1. Tổng quan

| Thuộc tính | Giá trị |
|-----------|---------|
| **File** | `data/survey_responses_raw.csv` |
| **Mô tả** | Khảo sát nhu cầu học Data thực tế của người dùng nền tảng DUA Edu |
| **Số dòng** | 210 (không tính header) |
| **Số cột** | 13 |
| **Thời gian thu thập** | 29/10/2026 – 14/11/2026 |
| **Encoding** | UTF-8 |

---

## 2. Data Schema

| # | Tên cột | Kiểu dữ liệu | Nullable | Mô tả |
|---|---------|--------------|----------|-------|
| 1 | `timestamp` | `datetime` | Không | Thời điểm người dùng gửi phản hồi. Định dạng: `DD/MM/YYYY HH:MM:SS` |
| 2 | `email_address` | `text` | Có (10) | Địa chỉ email người dùng. |
| 3 | `current_role` | `text` (single-select) | Không | Vai trò / nghề nghiệp hiện tại của người dùng |
| 4 | `primary_goal` | `text` (multi-select) | Không | Mục tiêu chính khi sử dụng nền tảng DUA Edu |
| 5 | `desired_courses` | `text` (multi-select) | Có (1) | Nội dung khóa học / kỹ năng mong muốn được đào tạo |
| 6 | `pain_points` | `text` (multi-select / free-text) | Không | Khó khăn, rào cản khi tự học Data |
| 7 | `source` | `text` (single-select / free-text) | Không | Kênh tiếp cận — người dùng biết đến DUA Edu qua đâu |
| 8 | `selection_criteria` | `text` (multi-select) | Có (2) | Tiêu chí quan trọng khi chọn nền tảng học Data |
| 9 | `desired_layout` | `text` (single-select / free-text) | Không | Mô hình giao diện sản phẩm mong muốn |
| 10 | `exp_score` | `integer` (1–5) | Không | Điểm đánh giá trải nghiệm sử dụng nền tảng (1 = rất không hài lòng, 5 = rất hài lòng) |
| 11 | `ui_ux_score` | `integer` (1–5) | Không | Điểm đánh giá giao diện / trải nghiệm người dùng (1 = rất không hài lòng, 5 = rất hài lòng) |
| 12 | `negative_feedback` | `text` (free-text) | Có (78) | Phản hồi tiêu cực, điểm chưa hài lòng về nền tảng |
| 13 | `improvement_suggestion` | `text` (free-text) | Có (80) | Đề xuất cải thiện từ người dùng |

---

## 3. Chi tiết giá trị từng cột

### 3.1 `current_role` — Vai trò hiện tại

| Giá trị | Số lượng |
|---------|---------|
| Sinh viên | 121 |
| Người đi làm muốn học thêm kĩ năng Phân tích dữ liệu | 55 |
| Người đi làm muốn chuyển sang nghề Data Analyst | 21 |
| Data Analyst | 6 |
| Khác (free-text: AI Engineer, Data Engineer, BA, thất nghiệp...) | 7 |

### 3.2 `primary_goal` — Mục tiêu chính (multi-select)

Các giá trị phổ biến (phân tách bằng dấu phẩy):

- Học kiến thức Data nền tảng
- Thực hành trên bài toán thực tế
- Phát triển tư duy phân tích dữ liệu
- Học thêm công cụ phân tích dữ liệu (SQL, PowerBI,...)
- Làm dự án / xây portfolio
- Chuyển ngành / tìm việc trong lĩnh vực Data
- Phục vụ công việc hiện tại
- Học theo lộ trình bài bản
- Chuẩn bị phỏng vấn
- Tham gia cộng đồng, duy trì động lực học
- Nhận các quyền lợi / quà tặng / ưu đãi từ DUA Edu

### 3.3 `desired_courses` — Nội dung mong muốn (multi-select)

Các giá trị phổ biến:

- Học tư duy dữ liệu
- Công cụ phân tích dữ liệu
- Domain knowledge cho DA
- Giải các case study thực tế
- Luyện phỏng vấn interview
- Luyện thi chứng chỉ
- AI ứng dụng dành cho DA

### 3.4 `pain_points` — Khó khăn khi tự học (multi-select / free-text)

Các giá trị phổ biến:

- Thiếu roadmap
- Thiếu dữ liệu thực tế và môi trường để thực hành
- Tài liệu và nội dung học quá khó hiểu
- Thiếu tài nguyên học tập (video, sách, bài tập, khóa học,...)
- Không có khó khăn gì đáng kể

> **Lưu ý:** Một số response chứa free-text dài thay vì chọn từ danh sách.

### 3.5 `source` — Kênh tiếp cận

| Nhóm | Giá trị gốc | Số lượng |
|------|-------------|---------|
| Group GenZ làm Data | `Group "GenZ làm Data"` | 135 |
| Thread | `Thread` | 38 |
| Group Zalo | `Qua group Zalo` | 12 |
| Người quen | `Người quen giới thiệu` | 7 |
| Facebook | `Facebook`, `facebook`, `Fb`, `Đề xuất Facebook`, `Group Facebook`... | ~10 |
| Chưa biết | `Chưa biết đến website` | 4 |
| Khác | Free-text cá nhân | ~4 |

> **Lưu ý:** Cột cần chuẩn hóa — nhiều biến thể cho cùng kênh Facebook.

### 3.6 `desired_layout` — Mô hình giao diện mong muốn

| Giá trị | Số lượng |
|---------|---------|
| Đơn giản, tập trung vào các đầu mục học tập chính và tối giản các tính năng | 112 |
| Nhiều tính năng, trò chơi thú vị, cân bằng giữa học và chơi | 50 |
| Tối giản nhưng vẫn giữ lại một số tính năng nhỏ để tạo ra sự thú vị khi học | 45 |
| Khác (free-text) | 3 |

### 3.7 `exp_score` & `ui_ux_score` — Điểm đánh giá

| Điểm | exp_score | ui_ux_score |
|------|-----------|-------------|
| 1 | 1 | 2 |
| 2 | 0 | 1 |
| 3 | 6 | 15 |
| 4 | 69 | 72 |
| 5 | 134 | 120 |
