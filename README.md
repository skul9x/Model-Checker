# 🚀 Gemini Key Inspector PRO (Go Version)

![Go](https://img.shields.io/badge/Language-Go-blue?logo=go)
![Wails](https://img.shields.io/badge/Framework-Wails_v2-red?logo=wails)
![Status](https://img.shields.io/badge/Status-Active-success)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey)

**Gemini Key Inspector PRO** là một công cụ mạnh mẽ được xây dựng bằng **Go** và framework **Wails**, cho phép người dùng trích xuất, kiểm tra và quản lý các API Key của Google Gemini một cách nhanh chóng và hiệu quả. Với sức mạnh của Goroutines, ứng dụng có thể xử lý hàng trăm key cùng lúc mà vẫn đảm bảo giao diện mượt mà.

---

## ✨ Tính năng chính

- **🔍 Trích xuất thông minh**: Tự động tìm kiếm các chuỗi API Key định dạng `AIza...` từ bất kỳ đoạn văn bản thô nào.
- **⚡ Kiểm tra đa luồng**: Sử dụng sức mạnh tối đa của CPU để xác minh tình trạng hoạt động (ACTIVE/ERROR) của hàng loạt key trong tích tắc.
- **📊 Thông tin chi tiết**: Hiển thị danh sách tất cả các AI Model mà mỗi Key được phép truy cập (Gemini 1.5 Pro, Flash, v.v.).
- **🧪 Test Model trực tiếp**: Cho phép gửi yêu cầu thử nghiệm ("hi") đến một model cụ thể để xác minh quyền thực thi thực tế.
- **🎨 Giao diện hiện đại**: Thiết kế theo phong cách Glassmorphism với chế độ tối (Dark Mode) mặc định, mang lại trải nghiệm chuyên nghiệp.
- **🌐 Việt hóa hoàn toàn**: Giao diện và thông báo lỗi được tối ưu riêng cho người dùng Việt Nam.

---

## 📂 Cấu trúc thư mục

```text
ModelChecker-Go/
├── build/              # Chứa các file build và asset nền tảng (icons, v.v.)
│   └── bin/            # Nơi chứa file thực thi sau khi build
├── frontend/           # Mã nguồn giao diện (Vite/Vanilla JS/CSS)
│   ├── src/            # Các file logic và giao diện chính
│   └── dist/           # File frontend đã được build (để nhúng vào Go)
├── scanner.go          # Logic cốt lõi: Regex, kiểm tra API, Goroutines
├── app.go              # Cầu nối (binding) giữa Go và Frontend
├── main.go             # Điểm khởi đầu của ứng dụng
├── wails.json          # Cấu hình dự án Wails
└── .brain/             # (Tùy chọn) Lưu trữ dữ liệu context của AI Assistant
```

---

## 🛠️ Hướng dẫn cài đặt (Dành cho nhà phát triển)

### Yêu cầu hệ thống:
1.  **Go** (Phiên bản 1.21 trở lên)
2.  **Node.js** & **npm** (Để build frontend)
3.  **Wails CLI**: Cài đặt bằng lệnh:
    ```bash
    go install github.com/wailsapp/wails/v2/cmd/wails@latest
    ```
4.  **Dependencies (Linux)**: Nếu bạn dùng Linux, hãy cài thêm:
    ```bash
    sudo apt install libgtk-3-dev libwebkit2gtk-4.1-dev
    ```

### Các bước cài đặt:
1.  Clone repository:
    ```bash
    git clone https://github.com/skul9x/Model-Checker.git
    cd ModelChecker-Go
    ```
2.  Cài đặt dependencies frontend:
    ```bash
    cd frontend && npm install && cd ..
    ```

---

## 🚀 Hướng dẫn sử dụng

1.  **Mở ứng dụng**: Chạy file `ModelChecker-Go.exe`.
2.  **Nhập dữ liệu**: Dán đoạn văn bản chứa API Key vào ô nhập liệu (có thể chứa nhiều nội dung rác, ứng dụng sẽ tự lọc).
3.  **Quét Key**: Nhấn nút "Bắt đầu quét". Kết quả sẽ hiển thị ngay lập tức trong bảng bên dưới.
4.  **Xem chi tiết**: Nhấn vào từng Key để xem danh sách Model khả dụng.
5.  **Thử nghiệm**: Nhấn nút "Kiểm tra" cạnh tên Model để xác minh xem Model đó có hoạt động thực tế hay không.

---

## 🏗️ Cách Build ứng dụng

### 1. Build file thực thi (.exe cho Windows)
Để đóng gói ứng dụng thành một file duy nhất:
```bash
wails build -platform windows/amd64
```
Kết quả sẽ nằm tại `build/bin/ModelChecker-Go.exe`.

### 2. Tạo bộ cài đặt (Installer)
Nếu bạn đã cài đặt **NSIS**, bạn có thể tạo bộ cài đặt chuyên nghiệp:
```bash
wails build -platform windows/amd64 -nsis
```

---

## 📜 Giấy phép & Bản quyền
Bản quyền © 2026 **Nguyễn Duy Trường**.
Sản phẩm được hỗ trợ phát triển bởi **Antigravity AI Assistant**.

---
*Chúc bạn có những trải nghiệm tuyệt vời với Gemini Key Inspector PRO!*
