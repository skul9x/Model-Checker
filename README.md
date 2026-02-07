# 🚀 Gemini Key Inspector Pro

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python&logoColor=white)
![PySide6](https://img.shields.io/badge/GUI-PySide6-green?style=flat-square&logo=qt&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-success?style=flat-square)

**Gemini Key Inspector Pro** is a powerful desktop utility designed for developers and AI researchers to bulk validate Google Gemini API keys. It automatically discovers available models for each key, displays detailed capabilities, and wraps everything in a stunning, commercial-grade dark interface.

## 🌟 Key Features

### ⚡ **Multi-Key Intelligence**
- **Bulk Validation**: Paste logs, JSON, or mixed text containing multiple `AIza...` keys. The tool smart-scans and extracts them automatically.
- **Concurrent Checking**: Validates dozens of keys simultaneously using multi-threading for lightning-fast results.

### 🎨 **Commercial-Grade UI/UX**
- **Modern Dark Theme**: A sleek, VS Code-inspired interface designed for extended use without eye strain.
- **Responsive Layout**: Split-screen design with adjustable panels to fit your workflow.
- **Rich Data Tree**: Organize results hierarchically (Key -> List of Available Models).

### 🛠️ **Advanced Interaction**
- **Smart Context Menu**: Right-click to copy specific data:
  - Copy API Key / Model Name
  - Copy Description
  - Copy Full Details
- **Multi-Selection**: Support for `Ctrl` + Click and `Shift` + Click to select and copy multiple items at once.
- **Real-Time Status**: Live progress bar and status updates keep you informed during large scans.

## 📦 Installation

1.  **Clone the Repository** (or download the source code):
    ```bash
    git clone https://github.com/your-username/gemini-key-inspector.git
    cd gemini-key-inspector
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: Primarily requires `PySide6` and `requests`)*

## 🚀 Usage

1.  **Run the Application**:
    ```bash
    python ModelChecker/main.py
    ```

2.  **Scan Keys**:
    - Paste your content (logs, config files, raw text) into the left **Input** panel.
    - Click **SCAN & CHECK KEYS**.

3.  **Analyze Results**:
    - **Active Keys** will appear in Green with a count of available models.
    - **Dead/quota-exceeded Keys** will show as Error in Red.
    - Expand any key to see the full list of models it can access, along with their descriptions.

4.  **Extract Data**:
    - Select one or more rows.
    - Right-click and choose **Copy** to export data to your clipboard.

## 📂 Project Structure

```
ModelChecker/
├── main.py            # Entry point & Controller logic
├── ui.py              # Modern UI components & Layout
├── core.py            # Core logic (Workers, Regex, API Calls)
└── requirements.txt   # Project dependencies
```

## 🤝 Contributing

Contributions are welcome! Feel free to submit a Pull Request or open an Issue if you have ideas for improvements.

---
*Built with ❤️ for the AI Community.*
