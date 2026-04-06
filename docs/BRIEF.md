# 💡 BRIEF: Test All Models - Kiểm Tra Hàng Loạt

**Ngày tạo:** 2026-04-06
**Loại:** Feature Enhancement cho ModelChecker-Go

---

## 1. VẤN ĐỀ CẦN GIẢI QUYẾT
Hiện tại người dùng phải ấn nút "Kiểm tra" từng model một → rất tốn thời gian khi có nhiều key và hàng chục models.

## 2. GIẢI PHÁP ĐỀ XUẤT
Thêm nút **"Kiểm tra tất cả"** để tự động ping toàn bộ models cùng lúc, sau đó hiện danh sách kết quả rõ ràng (model nào dùng được, model nào lỗi) kèm nút copy danh sách models hoạt động.

## 3. ĐỐI TƯỢNG SỬ DỤNG
- **Primary:** Người dùng app ModelChecker-Go

## 4. TÍNH NĂNG

### 🚀 MVP:
- [ ] Nút "Kiểm tra tất cả" ở thanh controls
- [ ] Chạy ping tuần tự/song song giới hạn cho tất cả models
- [ ] Hiển thị progress realtime: "Đang kiểm tra X/Y models..."
- [ ] Hiện danh sách kết quả: ✅ model dùng được / ❌ model lỗi
- [ ] Nút copy danh sách các model hoạt động
- [ ] Disable nút khi đang chạy

### 🎁 Phase 2 (Làm sau):
- [ ] Nút "Dừng kiểm tra" giữa chừng
- [ ] Tóm tắt thống kê cuối cùng

## 5. PHƯƠNG ÁN KỸ THUẬT
- **Frontend-only**: Loop qua tất cả models, gọi `TestModel()` có sẵn từ Go backend
- Concurrency: chạy batch 3-5 models song song để nhanh nhưng không spam API
- Không cần sửa Go code

## 6. ƯỚC TÍNH
- **Độ phức tạp:** Đơn giản
- **Files cần sửa:** `frontend/src/main.js`, `frontend/src/app.css`

## 7. BƯỚC TIẾP THEO
→ Code trực tiếp
