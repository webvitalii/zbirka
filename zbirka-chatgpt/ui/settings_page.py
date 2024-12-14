import os
import json
from pathlib import Path
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                              QLabel, QLineEdit, QPushButton, QMessageBox,
                              QComboBox, QSlider)
from PySide6.QtCore import Qt, Signal

class SettingsPage(QWidget):
    api_key_changed = Signal(str)
    model_changed = Signal(str)
    temperature_changed = Signal(float)
    
    def __init__(self):
        super().__init__()
        self.settings_file = Path(os.path.dirname(os.path.dirname(__file__))) / 'settings.json'
        self.models = {
            "gpt-4-turbo": "GPT-4 Turbo (Fast, Most Capable)",
            "gpt-4": "GPT-4 (Slow, Very Capable)",
            "gpt-3.5-turbo": "GPT-3.5 Turbo (Fast, Good Balance)",
            "gpt-3.5-turbo-16k": "GPT-3.5 Turbo 16K (Fast, Long Context)"
        }
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
        
        # Model selection section
        model_layout = QHBoxLayout()
        model_label = QLabel("Model:")
        self.model_selector = QComboBox()
        for model_id, model_name in self.models.items():
            self.model_selector.addItem(model_name, model_id)
        model_layout.addWidget(model_label)
        model_layout.addWidget(self.model_selector)
        layout.addLayout(model_layout)
        
        # Temperature section
        temp_layout = QHBoxLayout()
        temp_label = QLabel("Temperature:")
        self.temp_slider = QSlider(Qt.Horizontal)
        self.temp_slider.setMinimum(0)
        self.temp_slider.setMaximum(20)  # 0.0 to 2.0
        self.temp_slider.setValue(7)      # Default 0.7
        self.temp_slider.setTickPosition(QSlider.TicksBelow)
        self.temp_slider.setTickInterval(2)
        
        self.temp_value_label = QLabel("0.7")
        self.temp_value_label.setMinimumWidth(50)
        self.temp_desc_label = QLabel("(Balanced)")
        self.temp_desc_label.setMinimumWidth(100)
        
        self.temp_slider.valueChanged.connect(self.update_temp_label)
        
        temp_layout.addWidget(temp_label)
        temp_layout.addWidget(self.temp_slider)
        temp_layout.addWidget(self.temp_value_label)
        temp_layout.addWidget(self.temp_desc_label)
        layout.addLayout(temp_layout)
        
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
        
    def update_temp_label(self, value):
        temp = value / 10.0
        self.temp_value_label.setText(f"{temp:.1f}")
        
        # Update description based on temperature
        if temp <= 0.3:
            desc = "(Focused)"
        elif temp <= 0.7:
            desc = "(Balanced)"
        elif temp <= 1.2:
            desc = "(Creative)"
        else:
            desc = "(Random)"
        self.temp_desc_label.setText(desc)
        
    def load_settings(self):
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    api_key = settings.get('api_key', '')
                    model = settings.get('model', 'gpt-3.5-turbo')
                    temperature = settings.get('temperature', 0.7)
                    
                    self.api_key_input.setText(api_key)
                    
                    # Find and select the saved model
                    index = self.model_selector.findData(model)
                    if index >= 0:
                        self.model_selector.setCurrentIndex(index)
                    
                    # Set temperature slider
                    self.temp_slider.setValue(int(temperature * 10))
                    
                    if api_key:
                        self.status_label.setText("Settings loaded")
                        self.status_label.setStyleSheet("color: green;")
                        self.api_key_changed.emit(api_key)
                        self.model_changed.emit(model)
                        self.temperature_changed.emit(temperature)
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
                
            model = self.model_selector.currentData()
            temperature = self.temp_slider.value() / 10.0
            
            settings = {
                'api_key': api_key,
                'model': model,
                'temperature': temperature
            }
            
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=4)
            
            self.status_label.setText("Settings saved")
            self.status_label.setStyleSheet("color: green;")
            self.api_key_changed.emit(api_key)
            self.model_changed.emit(model)
            self.temperature_changed.emit(temperature)
            QMessageBox.information(self, "Success", "Settings saved successfully!")
            
        except Exception as e:
            self.status_label.setText("Error saving settings")
            self.status_label.setStyleSheet("color: red;")
            QMessageBox.critical(self, "Error", f"Failed to save settings: {str(e)}")
