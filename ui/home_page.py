from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        welcome_label = QLabel("Welcome to the Python GUI Application")
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        info_label = QLabel("This application allows you to perform various operations, including CSV file manipulation.")
        info_label.setWordWrap(True)
        layout.addWidget(welcome_label)
        layout.addWidget(info_label)
        layout.addStretch()
        self.setLayout(layout)