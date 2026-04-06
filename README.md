# 🚀 Model-Checker-Go

![Go](https://img.shields.io/badge/Language-Go-blue?logo=go)
![Wails](https://img.shields.io/badge/Framework-Wails_v2-red?logo=wails)
![Status](https://img.shields.io/badge/Status-Active-success)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey)

**Model-Checker-Go** là một ứng dụng Desktop chuyên nghiệp được xây dựng bằng **Go** và **Wails**. Ứng dụng cung cấp các công cụ mạnh mẽ để trích xuất tự động, kiểm tra hàng loạt và quản lý thông tin các API Key của Google Gemini một cách nhanh chóng. 

Giúp cho các nhà phát triển dễ dàng xác minh quyền và khả năng hoạt động của từng API Key một cách an toàn và tiện lợi.

---

## ✨ Tính năng nổi bật

- **🔍 Trích xuất tự động thông minh**: Ứng dụng tự động tìm kiếm các mẫu API Key dạng `AIza...` từ file log, JSON hoặc văn bản thô. Không giới hạn số lượng key cần trích xuất.
- **⚡ Kiểm tra đa luồng (Concurrent Testing)**: Tận dụng ưu điểm của Goroutines trong Go để chia nhỏ công việc, bắt nhanh tình trạng hoạt động (HOẠT ĐỘNG / LỖI) của hàng loạt key trong cùng một khoảng thời gian ngắn.
- **⚡ Kiểm tra tất cả (Test All Models)**: Thử nghiệm thực tế toàn bộ các Model khả dụng của tất cả API Key chỉ với một cú click chuột! Kết quả cập nhật realtime và báo cáo rõ ràng trạng thái.
- **📊 Hiển thị thông tin chi tiết**: Đối với mỗi key hoạt động, liệt kê danh sách toàn bộ các Model khả dụng (như Gemini 1.5 Pro, Flash...) và quyền hạn của nó.
- **📋 Quản lý tiện lợi**: Hỗ trợ sao chép nhanh chuỗi các Model hoạt động ổn định.
- **🎨 Giao diện Vibe Coding (Glassmorphism)**: Tối ưu UI/UX với phong cách hiện đại Glassmorphism, hiệu ứng chuyển cảnh mượt mà, dark mode đẹp mắt.
- **🌐 100% Tiếng Việt**: Toàn bộ hệ thống, hướng dẫn cũng như cảnh báo đều đã được Việt hóa.

---

## 💻 Công nghệ sử dụng

Ứng dụng được thiết kế theo kiến trúc ứng dụng Desktop lai (Hybrid Desktop App):
- **Core Backend**: `Go (Golang)` xử lý logic cốt lõi như Regex tách string, Call API đồng thời qua hệ thống Goroutines tối ưu tốc độ và tiết kiệm bộ nhớ.
- **Desktop Framework**: `Wails v2` đóng gói Web frontend vào trong Native Window mượt mà.
- **Frontend UI**: Thiết kế thuần `Vanilla JS`, `HTML` và `CSS`. Không cần framework cồng kềnh nhằm giữ dung lượng file nhẹ nhất và khởi động trong tíc tắc.

---

## 📂 Thực đơn / Cấu trúc thư mục

```text
Model-Checker-Go/
├── build/              # Các biên dịch viên của hệ thống và assets
├── docs/               # Chứa các tài liệu phát triển (API, Brief...)
├── frontend/           # Toàn bộ mã nguồn giao diện
│   ├── src/            # File JS, CSS gốc (main.js, app.css)
│   └── dist/           # Thư mục web build (vite) để Wails inject
├── scanner.go          # Chứa logic backend (tìm Regex, hàm Ping API)
├── app.go              # Kết nối giữa Frontend (JS) và Backend (Go)
├── main.go             # Entry point (file khởi chạy gốc) của hệ thống
├── go.mod / wails.json # File cấu hình thư viện Go và Wails 
└── .brain/             # Setup tư duy và lịch sử làm việc của AI
```

---

## 🛠️ Hướng dẫn cài đặt

Bạn cần có một môi trường chuẩn bị sẵn để compile từ source code:

1. Dọn dẹp máy tính với [Go (>= 1.21)](https://go.dev/dl/) và [Node.js](https://nodejs.org/).
2. Cài đặt framework Wails CLI:
   ```bash
   go install github.com/wailsapp/wails/v2/cmd/wails@latest
   ```
3. *(Dành riêng cho Linux)*: Bạn cần gói thư viện webview
   ```bash
   sudo apt install libgtk-3-dev libwebkit2gtk-4.1-dev
   ```
4. Clone repo về máy:
   ```bash
   git clone https://github.com/skul9x/Model-Checker.git
   cd Model-Checker
   ```
5. Chạy môi trường dev để code khởi động realtime:
   ```bash
   wails dev
   ```

---

## 🚀 Cách sử dụng ứng dụng

1. **Khởi chạy ứng dụng**, giao diện màn hình nhập văn bản sẽ hiện ra.
2. Tại khu vực đầu vào, paste/dán những mã JSON, log chứa rất nhiều nội dung lộn xộn. (App sẽ tự dùng Regex bắt từ `AIza...`).
3. Click thanh **QUÉT & KIỂM TRA KEY**.
4. Lúc này danh sách Key đã được phân loại (Hoạt động hay chết). 
5. Tại panel KEY CÒN SỐNG: bạn có thể bấm Test riêng lẻ cho từng Model, HOẶC ấn **⚡ KIỂM TRA TẤT CẢ** để chạy trọn bộ 1 lần cho lẹ.
6. Kết thúc, ứng dụng có nút Copy Model list cho bạn chuyển sang tool khác nhẹ nhàng. 

---

## 🛡️ Vấn đề Bảo mật & API Key
- **Quy tắc An Toàn**: File mã nguồn (được public trên github) tuyệt đối KHÔNG chứa bất cứ API Key hợp lệ nào (VD: các chuỗi khởi đầu bằng `AIza...`). Mã nguồn đã được team kiểm duyệt nghiêm ngặt.
- Github Repo cũng có file `.gitignore` đầy đủ để không bị lọt rác ra ngoài hệ thống.

---

## 📜 Giấy phép & Bản quyền

Copyright 2026 Nguyễn Duy Trường

Mã nguồn được phân phối độc quyền. Mọi quyền được bảo lưu. Việc sử dụng, sao chép hoặc phân phối lại không có sự cho phép sẽ vi phạm thỏa thuận quyền sở hữu.
