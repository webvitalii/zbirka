from PySide6.QtWidgets import QWidget, QLineEdit, QPushButton, QVBoxLayout

class WhoisPage(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.text_input = QLineEdit()
        self.layout.addWidget(self.text_input)

        self.submit_btn = QPushButton("Whois class")
        self.layout.addWidget(self.submit_btn)

        self.setLayout(self.layout)