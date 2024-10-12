import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QStackedLayout)
from PySide6.QtGui import QIcon, QAction
from ui.csv_page import CsvPage
from ui.home_page import HomePage
from ui.json_page import JSONPage
from ui.web_analyzer_page import WebAnalyzerPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python GUI")
        self.setFixedSize(800, 600)  # width, height
        self.setWindowIcon(QIcon('assets/icon-ua-flag.ico'))
        
        self.content_layout = QStackedLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.content_layout)
        self.setCentralWidget(self.central_widget)

        self.create_menu()
        
        self.home_page = HomePage()
        self.csv_page = CsvPage()
        self.json_page = JSONPage()
        self.web_analyzer_page = WebAnalyzerPage()  # Add this line
        self.content_layout.addWidget(self.home_page)
        self.content_layout.addWidget(self.csv_page)
        self.content_layout.addWidget(self.json_page)
        self.content_layout.addWidget(self.web_analyzer_page)  # Add this line

        # Set the home page as the default view
        self.content_layout.setCurrentWidget(self.home_page)

    def create_menu(self):
        menu = self.menuBar()
        file_menu = menu.addMenu('File')
        tools_menu = menu.addMenu('Tools')

        home_action = QAction('Home', self)
        home_action.triggered.connect(self.show_home)
        file_menu.addAction(home_action)

        csv_action = QAction('CSV', self)
        csv_action.triggered.connect(self.show_csv)
        tools_menu.addAction(csv_action)

        json_action = QAction('JSON', self)
        json_action.triggered.connect(self.show_json)
        tools_menu.addAction(json_action)

        web_analyzer_action = QAction('Web Analyzer', self)  # Add this action
        web_analyzer_action.triggered.connect(self.show_web_analyzer)
        tools_menu.addAction(web_analyzer_action)

    def show_home(self):
        self.content_layout.setCurrentWidget(self.home_page)
        
    def show_csv(self):
        self.content_layout.setCurrentWidget(self.csv_page)

    def show_json(self):
        self.content_layout.setCurrentWidget(self.json_page)

    def show_web_analyzer(self):  # Add this method
        self.content_layout.setCurrentWidget(self.web_analyzer_page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion") # ['Breeze', 'Oxygen', 'QtCurve', 'Windows', 'Fusion']
    app.setStyleSheet('''
                      QPushButton { font-size: 20px; }
                      ''')
    window = MainWindow()
    window.show()
    sys.exit(app.exec())