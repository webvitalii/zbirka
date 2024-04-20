from PySide6.QtWidgets import QWidget, QLineEdit, QTextEdit, QPushButton, QVBoxLayout

class CsvPage(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.select_csv_file_btn = QPushButton("Select CSV file")
        self.select_csv_file_btn.clicked.connect(self.select_csv_file)
        self.layout.addWidget(self.select_csv_file_btn)
        
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Enter CSV fields to export in new file")
        self.layout.addWidget(self.text_input)
        
        self.create_csv_file_btn = QPushButton("Create new CSV file")
        self.create_csv_file_btn.clicked.connect(self.create_new_csv_file)
        self.layout.addWidget(self.create_csv_file_btn)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.layout.addWidget(self.output_text)

        self.setLayout(self.layout)
        
        
    def select_csv_file(self):
        pass
            
    def create_new_csv_file(self):
        pass
