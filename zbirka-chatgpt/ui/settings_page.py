import os
import json
from pathlib import Path
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                              QLabel, QLineEdit, QPushButton, QMessageBox)
from PySide6.QtCore import Qt, Signal

class SettingsPage(QWidget):
    api_key_changed = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.settings_file = Path(os.path.dirname(os.path.dirname(__file__))) / 'settings.json'
        self.setup_ui()
        self.load_settings()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Settings")
        title.setStyleSheet("font-size: 24px; margin: 20px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # API Key section
        api_key_layout = QHBoxLayout()
        api_key_label = QLabel("OpenAI API Key:")
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.Password)
        self.api_key_input.setMinimumWidth(400)
        api_key_layout.addWidget(api_key_label)
        api_key_layout.addWidget(self.api_key_input)
        layout.addLayout(api_key_layout)
        
        # Save button
        save_layout = QHBoxLayout()
        save_layout.addStretch()
        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(self.save_settings)
        save_layout.addWidget(self.save_button)
        layout.addLayout(save_layout)
        
        # Status label
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        self.setLayout(layout)
        
    def load_settings(self):
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    api_key = settings.get('api_key', '')
                    self.api_key_input.setText(api_key)
                    
                    if api_key:
                        self.status_label.setText("Settings loaded")
                        self.status_label.setStyleSheet("color: green;")
                        self.api_key_changed.emit(api_key)
            else:
                self.status_label.setText("No settings found")
                self.status_label.setStyleSheet("color: gray;")
        except Exception as e:
            self.status_label.setText("Error loading settings")
            self.status_label.setStyleSheet("color: red;")
            QMessageBox.warning(self, "Error", f"Failed to load settings: {str(e)}")
    
    def save_settings(self):
        try:
            api_key = self.api_key_input.text().strip()
            if not api_key:
                QMessageBox.warning(self, "Warning", "Please enter an API key")
                return
                
            settings = {
                'api_key': api_key
            }
            
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=4)
            
            self.status_label.setText("Settings saved")
            self.status_label.setStyleSheet("color: green;")
            self.api_key_changed.emit(api_key)
            QMessageBox.information(self, "Success", "Settings saved successfully!")
            
        except Exception as e:
            self.status_label.setText("Error saving settings")
            self.status_label.setStyleSheet("color: red;")
            QMessageBox.critical(self, "Error", f"Failed to save settings: {str(e)}")
