# Changelog - ModelChecker-Go

Toàn bộ lịch sử thay đổi của dự án Gemini Key Inspector Pro (Phiên bản Go).

## [1.1.0] - 2026-03-17
### Added
- Tính năng **Kiểm tra Model (Active Ping)**: Gửi prompt "hi" để xác minh model thực sự hoạt động.
- Hiển thị phản hồi thực tế từ model khi kiểm tra thành công.
- Icon ✅/❌ và thông báo lỗi chi tiết cho từng model.

### Changed
- **Việt hóa hoàn toàn**: Chuyển đổi toàn bộ UI và thông báo lỗi sang tiếng Việt.
- Cập nhật thông tin bản quyền: **© 2026 Nguyễn Duy Trường**.

## [1.0.0] - 2026-03-17
### Added
- **Migration**: Chuyển đổi từ Python (PySide6) sang Go (Wails v2).
- **Backend**: Xử lý trích xuất key bằng Regex và kiểm tra song song bằng Goroutines.
- **Frontend**: Giao diện Dark Mode hiện đại với Glassmorphism.
- Tự động phát hiện models khả dụng cho từng API Key.
- Chức năng Copy API Key nhanh qua menu chuột phải.
