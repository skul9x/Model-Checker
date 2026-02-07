
import sys
from PySide6.QtWidgets import QApplication, QTreeWidgetItem, QMessageBox, QMenu
from PySide6.QtCore import QThreadPool, Slot
from PySide6.QtGui import QColor, QAction

# Internal imports
try:
    from ui import ModernWindow
    from core import extract_api_keys, KeyDiscoveryWorker
except ImportError:
    # Handle running from parent directory
    from ModelChecker.ui import ModernWindow
    from ModelChecker.core import extract_api_keys, KeyDiscoveryWorker

class AppController(ModernWindow):
    def __init__(self):
        super().__init__()
        self.threadpool = QThreadPool()
        print(f"Running with max {self.threadpool.maxThreadCount()} threads")
        
        # Connection
        self.btn_check.clicked.connect(self.start_scan)
        self.result_tree.customContextMenuRequested.connect(self.show_context_menu)
        
        # State
        self.total_keys = 0
        self.processed_keys = 0
        self.active_keys_count = 0

    def start_scan(self):
        text = self.input_text.toPlainText()
        keys = extract_api_keys(text)
        
        if not keys:
            QMessageBox.warning(self, "No Keys Found", 
                                "Could not find any 'AIza...' format keys in the input.")
            return

        # Reset UI
        self.result_tree.clear()
        self.processed_keys = 0
        self.total_keys = len(keys)
        self.active_keys_count = 0
        self.update_stats()
        
        self.progress_bar.show()
        self.progress_bar.setRange(0, self.total_keys)
        self.progress_bar.setValue(0)
        
        self.btn_check.setEnabled(False)
        self.status_label_top.setText(f"Scanning {self.total_keys} keys...")

        # Spawn Workers
        for key in keys:
            worker = KeyDiscoveryWorker(key)
            worker.signals.result.connect(self.handle_worker_result)
            worker.signals.finished.connect(self.handle_worker_finished)
            self.threadpool.start(worker)

    @Slot(str, list, str)
    def handle_worker_result(self, key, models, error):
        # Create Root Item for Key
        masked_key = f"{key[:6]}...{key[-4:]}"
        # key argument is the full key
        
        root = QTreeWidgetItem(self.result_tree)
        root.setText(0, masked_key)
        root.setData(0, 32, key) # Store full key in UserRole (32)
        
        if error:
            root.setText(1, "ERROR")
            root.setForeground(1, QColor("#F44336")) # Red
            root.setText(2, str(error))
            root.setExpanded(False)
        else:
            root.setText(1, "ACTIVE")
            root.setForeground(1, QColor("#4CAF50")) # Green
            root.setText(2, f"{len(models)} models found")
            self.active_keys_count += 1
            
            # Add Child Items (Models)
            for m in models:
                child = QTreeWidgetItem(root)
                child.setText(0, m['name'])
                child.setText(1, "Available")
                child.setText(2, m['description'])  # Show description in column 2
                child.setForeground(1, QColor("#888888"))
            
            root.setExpanded(True)

    @Slot()
    def handle_worker_finished(self):
        self.processed_keys += 1
        self.progress_bar.setValue(self.processed_keys)
        self.update_stats()
        
        if self.processed_keys >= self.total_keys:
            self.scan_finished()

    def scan_finished(self):
        self.btn_check.setEnabled(True)
        self.progress_bar.hide()
        self.status_label_top.setText("Scan Completed")
        QMessageBox.information(self, "Scan Complete", 
                                f"Finished checking {self.total_keys} keys.\n"
                                f"Active Keys: {self.active_keys_count}")

    def update_stats(self):
        self.lbl_stats.setText(f"Keys Found: {self.total_keys} | Checked: {self.processed_keys} | Active: {self.active_keys_count}")

    def show_context_menu(self, position):
        items = self.result_tree.selectedItems()
        if not items:
            return

        menu = QMenu()
        
        # Actions
        copy_name_action = QAction("Copy Local Name / Key", self)
        copy_name_action.triggered.connect(lambda: self.copy_to_clipboard(items, 0))
        
        copy_desc_action = QAction("Copy Description", self)
        copy_desc_action.triggered.connect(lambda: self.copy_to_clipboard(items, 2))
        
        copy_all_action = QAction("Copy Name & Description", self)
        copy_all_action.triggered.connect(lambda: self.copy_to_clipboard(items, "all"))

        menu.addAction(copy_name_action)
        menu.addAction(copy_desc_action)
        menu.addSeparator()
        menu.addAction(copy_all_action)
        
        menu.exec_(self.result_tree.viewport().mapToGlobal(position))

    def copy_to_clipboard(self, items, column):
        clipboard = QApplication.clipboard()
        text_list = []
        
        for item in items:
            # Skip if it is a Root Item (Key) and we want description (Column 2 is usually empty or Status)
            # Actually Root Item Col 2 is Status Msg (Active/Error).
            
            if column == "all":
                t0 = item.text(0)
                t2 = item.text(2)
                text_list.append(f"{t0} - {t2}")
            else:
                text_list.append(item.text(column))
        
        final_text = "\n".join(text_list)
        clipboard.setText(final_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set app style
    app.setStyle("Fusion")
    
    window = AppController()
    window.show()
    sys.exit(app.exec())
