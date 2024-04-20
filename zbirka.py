import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QMenu, QStackedLayout)
from PySide6.QtGui import QIcon, QAction
from ui.whois_page import WhoisPage
from ui.csv_page import CsvPage


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
        
        self.csv_page = CsvPage()
        self.content_layout.addWidget(self.csv_page)
        
        self.whois_page = WhoisPage()
        self.content_layout.addWidget(self.whois_page)


    def create_menu(self):
        menu = self.menuBar()
        file_menu = menu.addMenu('File')
        tools_menu = menu.addMenu('Tools')

        impMenu = QMenu('Import', self)
        impAct = QAction('Import mail', self)
        impMenu.addAction(impAct)

        csv_action = QAction('CSV', self)
        csv_action.triggered.connect(self.show_csv)
        
        whois_action = QAction("Whois", self)
        whois_action.triggered.connect(self.show_whois)

        file_menu.addMenu(impMenu)
        tools_menu.addAction(csv_action)
        tools_menu.addAction(whois_action)
        

    def show_whois(self):
        self.content_layout.setCurrentWidget(self.whois_page)
        
    def show_csv(self):
        self.content_layout.setCurrentWidget(self.csv_page)

    def sayHi(self):
        inputText = self.inputField.text()
        self.textField.setText(f"Hi, {inputText}!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion") # ['Breeze', 'Oxygen', 'QtCurve', 'Windows', 'Fusion']
    app.setStyleSheet('''
                      QPushButton { font-size: 20px; }
                      ''')
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
