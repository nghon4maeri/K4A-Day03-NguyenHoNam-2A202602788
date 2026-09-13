# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** Nguyễn Hồ Nam  
> **Mã Sinh Viên / Mã Học viên:** 2A202602788  
> **Chủ đề Lựa chọn:** Trợ lý Học vụ & Tra cứu Lịch thi VinUni (Gợi ý 1.1 — Lĩnh vực Giáo dục)  

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** | 4 / 5 | Bài toán có chuỗi suy luận nối tiếp: trước khi đặt lịch tư vấn, Agent cần tra cứu hồ sơ để xác định đúng cố vấn học tập của sinh viên (Test Case TC04). Câu hỏi tra cứu và đặt lịch đều yêu cầu nhiều bước quyết định liên tiếp nhau. |
| **2. Tool Interaction** | 5 / 5 | Hệ thống bắt buộc kết nối MCP Server / Cơ sở dữ liệu bên ngoài để tra cứu hồ sơ sinh viên (`academic_query`) và thực hiện hành động đặt lịch (`schedule_appointment`). Không có Tool thì Agent không thể trả lời dữ liệu thời gian thực. |
| **3. Dynamic Decision** | 4 / 5 | Bước tiếp theo phụ thuộc vào kết quả quan sát bước trước: nếu tra cứu trả về `NOT_FOUND` thì không đặt lịch mà phản hồi lịch sự (TC05); nếu `SUCCESS` thì lấy tên cố vấn thật để đặt lịch (TC04). |
| **4. Long Horizon Goal** | 3 / 5 | Mục tiêu trải qua nhiều lượt xử lý trong cùng một phiên hội thoại: sinh viên có thể tra cứu hồ sơ, sau đó yêu cầu đặt lịch với cùng ngữ cảnh. Chưa cần duy trì mục tiêu qua nhiều ngày nên chấm 3/5. |
| **TỔNG ĐIỂM AGENTIC FIT** | **16 / 20** | *Tổng điểm > 12/20: Bài toán rất phù hợp triển khai Agentic System.* |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (SAU KHI CHẠY TEST SUITE TRÊN API THẬT)

> ⚠️ **YÊU CẦU NGHIỆM THU:** Mở tệp `.env` điền `GEMINI_API_KEY` (hoặc `OPENAI_API_KEY`) để kết nối LLM thật trước khi thực thi `python src/app.py --all`. Bài nộp chỉ dùng Mock Offline Provider sẽ không đạt điểm nghiệm thực tế.

Dán 1 đoạn trích xuất log tiêu biểu từ file `docs/trace_waterfall.json` sinh ra từ phản hồi LLM API thật (chuỗi ReAct đa bước TC04: Tra cứu -> Đặt lịch):

```json
[
  {
    "step": 1,
    "query": "Hãy tra cứu thông tin của sinh viên SV2026002 để biết cố vấn học tập của bạn ấy, sau đó đặt lịch hẹn tư vấn với đúng cố vấn đó vào lúc 09:30 ngày 16/09/2026.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "academic_query",
    "arguments": { "student_id": "SV2026002" },
    "observation": {
      "status": "SUCCESS",
      "student_id": "SV2026002",
      "data": {
        "full_name": "Trần Thị Bình",
        "class": "AI-K4",
        "gpa": 3.6,
        "email": "binh.tt@vinuni.edu.vn",
        "status": "Đang học",
        "advisor": "TS. Lê Thị B"
      }
    },
    "latency_ms": 4425.05
  },
  {
    "step": 2,
    "query": "Hãy tra cứu thông tin của sinh viên SV2026002 để biết cố vấn học tập của bạn ấy, sau đó đặt lịch hẹn tư vấn với đúng cố vấn đó vào lúc 09:30 ngày 16/09/2026.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "schedule_appointment",
    "arguments": {
      "student_id": "SV2026002",
      "datetime_str": "09:30 16/09/2026",
      "advisor_name": "TS. Lê Thị B"
    },
    "observation": {
      "status": "SUCCESS",
      "booking_id": "BK-SV2026002-99",
      "student_id": "SV2026002",
      "datetime": "09:30 16/09/2026",
      "advisor": "TS. Lê Thị B",
      "message": "Đặt lịch thành công cho sinh viên SV2026002 với TS. Lê Thị B vào lúc 09:30 16/09/2026."
    },
    "latency_ms": 1689.42
  },
  {
    "step": 3,
    "query": "Hãy tra cứu thông tin của sinh viên SV2026002 để biết cố vấn học tập của bạn ấy, sau đó đặt lịch hẹn tư vấn với đúng cố vấn đó vào lúc 09:30 ngày 16/09/2026.",
    "action_type": "FINAL_ANSWER",
    "thought": "OpenAI phản hồi trực tiếp bằng văn bản (không cần gọi công cụ).",
    "output": "Tôi đã thực hiện xong cả hai yêu cầu của bạn. ... Cố vấn: TS. Lê Thị B - Thời gian: 09:30 ngày 16/09/2026 ...",
    "latency_ms": 2528.05
  }
]
```

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [x] Đã điền API Key thật trong `.env` và xác nhận Agent chạy mượt mà trên LLM API thật (OpenAI-compatible Fireworks AI: `deepseek-v4-flash-0731`).
- **Tổng số Test Cases đã chạy thành công:** 5 / 5 test cases (chạy bằng `python src/app.py --all` với LLM API thật).
- **Số lượt gọi Tool qua MCP Server chính xác:** 5 lượt (TC02: `academic_query`, TC03: `schedule_appointment`, TC04: `academic_query` → `schedule_appointment`, TC05: `academic_query` trả `NOT_FOUND`).
- **Kết quả đẩy Repo nộp bài:** [x] Đã Commit và Push mã nguồn thành công lên GitHub cá nhân (https://github.com/nghon4maeri/K4A-Day03-NguyenHoNam-2A202602788).

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!
