# API Documentation (Wails Bindings)

Tài liệu về các hàm Backend (Go) có thể gọi từ Frontend (JS).

---

## 🔍 App.ScanKeys
Trích xuất và kiểm tra hàng loạt API Key từ văn bản.

**Request (JS):**
```javascript
const results = await window.go.main.App.ScanKeys(longText);
```

**Response (Array of Object):**
```json
[
  {
    "key": "AIza...",
    "status": "ACTIVE",
    "models": [
      { "name": "models/gemini-1.5-flash", "description": "..." }
    ],
    "error": ""
  }
]
```

---

## ⚡ App.TestModel
Kiểm tra khả năng phản hồi của một model cụ thể.

**Request (JS):**
```javascript
const response = await window.go.main.App.TestModel(apiKey, modelName);
```

**Response (String):**
- Trả về nội dung phản hồi từ model (ví dụ: "Hello there!")
- Ném ra lỗi (Exception) nếu thất bại (429, 403, lỗi kết nối...).

---

## 📝 Quy tắc Logic
- **Regex trích xuất:** `AIza[0-9A-Za-z\-_]{35}`
- **Concurrency:** Mỗi key được kiểm tra trong một Gorountine riêng biệt.
- **Timeout:** 10s cho ScanKeys, 15s cho TestModel.
