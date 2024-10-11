import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QStackedLayout)
from PySide6.QtGui import QIcon, QAction
from ui.csv_page import CsvPage
from ui.home_page import HomePage

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
        self.content_layout.addWidget(self.home_page)
        self.content_layout.addWidget(self.csv_page)

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

    def show_home(self):
        self.content_layout.setCurrentWidget(self.home_page)
        
    def show_csv(self):
        self.content_layout.setCurrentWidget(self.csv_page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion") # ['Breeze', 'Oxygen', 'QtCurve', 'Windows', 'Fusion']
    app.setStyleSheet('''
                      QPushButton { font-size: 20px; }
                      ''')
    window = MainWindow()
    window.show()
    sys.exit(app.exec())