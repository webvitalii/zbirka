from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        welcome_label = QLabel("Welcome to ChatGPT Desktop")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 24px; margin: 20px;")
        
        description = QLabel("Access ChatGPT through the Tools menu to start chatting!")
        description.setAlignment(Qt.AlignCenter)
        description.setStyleSheet("font-size: 16px;")
        
        layout.addWidget(welcome_label)
        layout.addWidget(description)
        layout.addStretch()
        
        self.setLayout(layout)