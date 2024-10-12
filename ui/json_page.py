import json
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                               QTextEdit, QFileDialog, QMessageBox)

class JSONPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # JSON content area
        self.json_edit = QTextEdit()
        self.json_edit.setPlaceholderText("Enter JSON here or load a file...")
        layout.addWidget(self.json_edit)

        # Buttons
        button_layout = QHBoxLayout()
        self.load_button = QPushButton("Load JSON")
        self.save_button = QPushButton("Save JSON")
        self.format_button = QPushButton("Format JSON")
        self.load_button.clicked.connect(self.load_json)
        self.save_button.clicked.connect(self.save_json)
        self.format_button.clicked.connect(self.format_json)
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.format_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def load_json(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open JSON File", "", "JSON Files (*.json)")
        if file_name:
            try:
                with open(file_name, 'r') as file:
                    json_content = json.load(file)
                    self.json_edit.setPlainText(json.dumps(json_content, indent=4))
            except json.JSONDecodeError:
                QMessageBox.warning(self, "Error", "Invalid JSON file")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")

    def save_json(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save JSON File", "", "JSON Files (*.json)")
        if file_name:
            try:
                json_content = json.loads(self.json_edit.toPlainText())
                with open(file_name, 'w') as file:
                    json.dump(json_content, file, indent=4)
                QMessageBox.information(self, "Success", "JSON file saved successfully")
            except json.JSONDecodeError:
                QMessageBox.warning(self, "Error", "Invalid JSON content")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")

    def format_json(self):
        try:
            json_content = json.loads(self.json_edit.toPlainText())
            formatted_json = json.dumps(json_content, indent=4)
            self.json_edit.setPlainText(formatted_json)
        except json.JSONDecodeError:
            QMessageBox.warning(self, "Error", "Invalid JSON content")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")