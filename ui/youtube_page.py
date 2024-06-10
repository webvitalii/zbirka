from PySide6.QtWidgets import QWidget, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QLabel
from PySide6.QtCore import QUrl
import youtube_dl

class YoutubePage(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.url_label = QLabel("Enter YouTube URL")
        self.layout.addWidget(self.url_label)

        self.text_input = QLineEdit()
        self.layout.addWidget(self.text_input)

        self.download_btn = QPushButton("Download Video")
        self.download_btn.clicked.connect(self.download_video)
        self.layout.addWidget(self.download_btn)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.layout.addWidget(self.output_text)

        self.setLayout(self.layout)
        
    def download_video(self):
        url = self.text_input.text()

        # Validate URL format
        if not QUrl(url).isValid():
            self.output_text.setText("Invalid URL format. Please enter a valid YouTube URL.")
            return

        # Check if the URL is a YouTube URL
        if "youtube.com" not in url and "youtu.be" not in url:
            self.output_text.setText("Please enter a valid YouTube URL.")
            return

        try:
            ydl_opts = {'verbose': True}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.output_text.setText("Download completed successfully.")
        except Exception as e:
            self.output_text.setText(f"Failed to download video: {str(e)}")
