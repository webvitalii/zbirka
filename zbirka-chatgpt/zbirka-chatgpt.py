import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PySide6.QtGui import QAction
from ui.chatgpt_page import ChatGPTPage
from ui.settings_page import SettingsPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zbirka ChatGPT")
        self.setMinimumSize(800, 600)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)
        
        # Create pages
        self.chatgpt_page = ChatGPTPage()
        self.settings_page = SettingsPage()
        
        # Connect settings page signals to ChatGPT page
        self.settings_page.api_key_changed.connect(self.chatgpt_page.update_api_key)
        self.settings_page.model_changed.connect(self.chatgpt_page.update_model)
        
        # Show ChatGPT page by default
        self.layout.addWidget(self.chatgpt_page)
        self.chatgpt_page.show()
        self.settings_page.hide()
        
        # Create menu bar
        self.create_menu_bar()
        
    def create_menu_bar(self):
        menu_bar = self.menuBar()
        tools_menu = menu_bar.addMenu("Tools")
        
        # ChatGPT action
        chatgpt_action = QAction("ChatGPT", self)
        chatgpt_action.triggered.connect(self.show_chatgpt)
        tools_menu.addAction(chatgpt_action)
        
        # Settings action
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.show_settings)
        tools_menu.addAction(settings_action)
        
    def show_chatgpt(self):
        self.settings_page.hide()
        self.layout.removeWidget(self.settings_page)
        self.layout.addWidget(self.chatgpt_page)
        self.chatgpt_page.show()
        
    def show_settings(self):
        self.chatgpt_page.hide()
        self.layout.removeWidget(self.chatgpt_page)
        self.layout.addWidget(self.settings_page)
        self.settings_page.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion") # ['Breeze', 'Oxygen', 'QtCurve', 'Windows', 'Fusion']
    app.setStyleSheet('''
                      QPushButton { font-size: 20px; }
                      ''')
    window = MainWindow()
    window.show()
    sys.exit(app.exec())