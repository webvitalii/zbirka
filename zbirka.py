import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QMenu)
from PyQt6.QtGui import QIcon, QAction


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python GUI")
        self.setFixedSize(800, 600) # width, height
        self.setWindowIcon(QIcon('assets/icon-ua-flag.svg'))
        
        layout = QVBoxLayout()
        
        self.inputField = QLineEdit()
        self.textField = QTextEdit() # multiline text input
        self.button = QPushButton("Greet")
        self.button.clicked.connect(self.sayHi)
        layout.addWidget(self.inputField)
        layout.addWidget(self.textField)
        layout.addWidget(self.button)
        
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)
        
        menu = self.menuBar()
        fileMenu = menu.addMenu('File')

        impMenu = QMenu('Import', self)
        impAct = QAction('Import mail', self)
        impMenu.addAction(impAct)

        greetAct = QAction('Greet', self)
        greetAct.triggered.connect(self.sayHi)

        fileMenu.addAction(greetAct)
        fileMenu.addMenu(impMenu)
    
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
