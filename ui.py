
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QPlainTextEdit, QPushButton, QTreeWidget, QTreeWidgetItem, 
                               QLabel, QProgressBar, QSplitter, QFrame, QMenu)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QAction, QColor, QFont, QPalette

class DarkThemePalette(QPalette):
    def __init__(self):
        super().__init__()
        # VS Code Dark Theme Colors (Approx)
        dark_bg = QColor(30, 30, 30)
        lighter_bg = QColor(37, 37, 38)
        sidebar_bg = QColor(51, 51, 51)
        text_color = QColor(204, 204, 204)
        accent_color = QColor(0, 122, 204) # Blue
        selection_bg = QColor(9, 71, 113)
        
        self.setColor(QPalette.Window, dark_bg)
        self.setColor(QPalette.WindowText, text_color)
        self.setColor(QPalette.Base, lighter_bg)
        self.setColor(QPalette.AlternateBase, sidebar_bg)
        self.setColor(QPalette.ToolTipBase, QColor(255, 255, 220))
        self.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
        self.setColor(QPalette.Text, text_color)
        self.setColor(QPalette.Button, sidebar_bg)
        self.setColor(QPalette.ButtonText, text_color)
        self.setColor(QPalette.Link, accent_color)
        self.setColor(QPalette.Highlight, selection_bg)
        self.setColor(QPalette.HighlightedText, QColor(255, 255, 255))

class ModernWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gemini Key Inspector Pro")
        self.resize(1100, 750)
        self.setPalette(DarkThemePalette())

        # Main Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Header Bar
        self.header_frame = QFrame()
        self.header_frame.setStyleSheet("background-color: #333333; border-bottom: 1px solid #1E1E1E;")
        self.header_frame.setFixedHeight(50)
        header_layout = QHBoxLayout(self.header_frame)
        header_layout.setContentsMargins(15, 0, 15, 0)
        
        self.title_label = QLabel("🚀 Gemini Key Inspector")
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #FFFFFF;")
        
        self.status_label_top = QLabel("Ready")
        self.status_label_top.setStyleSheet("color: #AAAAAA;")
        self.status_label_top.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.status_label_top)
        
        main_layout.addWidget(self.header_frame)

        # 2. Content Area (Splitter: Input vs Result)
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setHandleWidth(1)
        self.splitter.setStyleSheet("QSplitter::handle { background-color: #444444; }")
        
        # Left Panel: Input
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(15, 15, 15, 15)
        
        input_label = QLabel("INPUT KEYS")
        input_label.setStyleSheet("font-weight: bold; color: #CCCCCC; margin-bottom: 5px;")
        
        self.input_text = QPlainTextEdit()
        self.input_text.setPlaceholderText("Paste your text containing API Keys here...\n(Support mixed content, JSON, logs, etc.)")
        self.input_text.setStyleSheet("""
            QPlainTextEdit {
                background-color: #1E1E1E;
                color: #D4D4D4;
                border: 1px solid #3E3E3E;
                font-family: Consolas, 'Courier New', monospace;
                font-size: 13px;
            }
        """)
        
        self.btn_check = QPushButton("SCAN & CHECK KEYS")
        self.btn_check.setFixedHeight(40)
        self.btn_check.setCursor(Qt.PointingHandCursor)
        self.btn_check.setStyleSheet("""
            QPushButton {
                background-color: #0E639C;
                color: white;
                border: none;
                font-weight: bold;
                border-radius: 2px;
            }
            QPushButton:hover { background-color: #1177BB; }
            QPushButton:pressed { background-color: #094771; }
            QPushButton:disabled { background-color: #3A3D41; color: #888888; }
        """)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(5)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar { background: #252526; border: none; }
            QProgressBar::chunk { background: #007ACC; }
        """)
        self.progress_bar.hide()

        left_layout.addWidget(input_label)
        left_layout.addWidget(self.input_text)
        left_layout.addWidget(self.progress_bar)
        left_layout.addWidget(self.btn_check)
        
        # Right Panel: Tree Result
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(15, 15, 15, 15)
        
        result_label = QLabel("RESULTS DASHBOARD")
        result_label.setStyleSheet("font-weight: bold; color: #CCCCCC; margin-bottom: 5px;")
        
        self.result_tree = QTreeWidget()
        self.result_tree.setHeaderLabels(["API Key / Model", "Status", "Details"])
        self.result_tree.setColumnWidth(0, 350)
        self.result_tree.setColumnWidth(1, 150)
        self.result_tree.setStyleSheet("""
            QTreeWidget {
                background-color: #252526;
                color: #CCCCCC;
                border: 1px solid #3E3E3E;
                font-size: 13px;
            }
            QTreeWidget::item { padding: 4px; }
            QTreeWidget::item:selected { background-color: #094771; }
            QHeaderView::section {
                background-color: #333333;
                color: #CCCCCC;
                padding: 4px;
                border: none;
                border-right: 1px solid #3E3E3E;
                border-bottom: 1px solid #3E3E3E;
            }
        """)

        self.result_tree.setContextMenuPolicy(Qt.CustomContextMenu)  # Enable Custom Context Menu
        self.result_tree.setSelectionMode(QTreeWidget.ExtendedSelection) # Enable Multi-Selection

        right_layout.addWidget(result_label)
        right_layout.addWidget(self.result_tree)

        self.splitter.addWidget(left_panel)
        self.splitter.addWidget(right_panel)
        self.splitter.setSizes([350, 750]) # Initial ratio

        main_layout.addWidget(self.splitter)

        # 3. Footer
        self.footer_frame = QFrame()
        self.footer_frame.setFixedHeight(25)
        self.footer_frame.setStyleSheet("background-color: #007ACC; color: white;")
        footer_layout = QHBoxLayout(self.footer_frame)
        footer_layout.setContentsMargins(10, 0, 10, 0)
        
        self.lbl_stats = QLabel("Keys Found: 0 | Checked: 0 | Active: 0")
        footer_layout.addWidget(self.lbl_stats)
        
        main_layout.addWidget(self.footer_frame)

    def contextMenuEvent(self, event):
        # Implement right-click if needed
        pass
