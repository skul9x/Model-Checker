# Phase 01: Cập nhật Backend (Go)

## Mục tiêu
Thêm hàm xử lý việc gửi prompt thử nghiệm đến model của Google Gemini.

## Các bước thực hiện
1. [ ] Thêm struct `TestRequest` và `TestResponse` cho API Google.
2. [ ] Viết hàm `TestModel(apiKey, modelName string)` trong `App` (app.go hoặc scanner.go).
3. [ ] Hàm này sẽ dùng POST request tới endpoint `generateContent`.
4. [ ] Trả về chuỗi kết quả đầu tiên hoặc thông báo lỗi cụ thể.

## Tệp cần sửa
- `scanner.go`
