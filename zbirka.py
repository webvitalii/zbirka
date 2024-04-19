import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QMenu, QStackedLayout)
from PySide6.QtGui import QIcon, QAction


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python GUI")
        self.setFixedSize(800, 600) # width, height
        self.setWindowIcon(QIcon('assets/icon-ua-flag.ico'))
        
        self.content_layout = QStackedLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.content_layout)
        self.setCentralWidget(self.central_widget)

        self.create_menu()
        
        self.greet_page = GreetPage()
        self.content_layout.addWidget(self.greet_page)
        
        self.whois_page = WhoisPage()
        self.content_layout.addWidget(self.whois_page)


    def create_menu(self):
        menu = self.menuBar()
        file_menu = menu.addMenu('File')
        tools_menu = menu.addMenu('Tools')

        impMenu = QMenu('Import', self)
        impAct = QAction('Import mail', self)
        impMenu.addAction(impAct)

        greet_action = QAction('Greet', self)
        greet_action.triggered.connect(self.show_greet)
        
        whois_action = QAction("Whois", self)
        whois_action.triggered.connect(self.show_whois)

        file_menu.addMenu(impMenu)
        tools_menu.addAction(greet_action)
        tools_menu.addAction(whois_action)
        

    def show_whois(self):
        self.content_layout.setCurrentWidget(self.whois_page)
        
    def show_greet(self):
        self.content_layout.setCurrentWidget(self.greet_page)

    def sayHi(self):
        inputText = self.inputField.text()
        self.textField.setText(f"Hi, {inputText}!")


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
        
        
class GreetPage(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.text_input = QLineEdit()
        self.layout.addWidget(self.text_input)

        self.submit_btn = QPushButton("Greet class")
        self.layout.addWidget(self.submit_btn)

        self.setLayout(self.layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion") # ['Breeze', 'Oxygen', 'QtCurve', 'Windows', 'Fusion']
    app.setStyleSheet('''
                      QPushButton { font-size: 20px; }
                      ''')
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
