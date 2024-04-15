import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTextEdit, QVBoxLayout
from PyQt6.QtGui import QIcon


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python GUI")
        self.setFixedSize(800, 600) # width, height
        self.setWindowIcon(QIcon('assets/icon-ua-flag.svg'))
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        self.inputField = QLineEdit()
        self.textField = QTextEdit() # multiline text input
        self.button = QPushButton("Greet")
        self.button.clicked.connect(self.sayHi)
        layout.addWidget(self.inputField)
        layout.addWidget(self.textField)
        layout.addWidget(self.button)
    
    def sayHi(self):
        inputText = self.inputField.text()
        self.textField.setText(f"Hi, {inputText}!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion") # ['Breeze', 'Oxygen', 'QtCurve', 'Windows', 'Fusion']
    app.setStyleSheet('''
                      QPushButton { font-size: 20px; }
                      ''')
    window = App()
    window.show()
    sys.exit(app.exec())
