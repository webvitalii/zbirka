import sys
import requests
import configparser
import markdown
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QScrollArea

API_ENDPOINT = "https://api.perplexity.ai/chat/completions"

def get_api_key():
    config = configparser.ConfigParser()
    config.read('pplx_config.ini')
    return config.get('PPLX', 'api_key')

API_KEY = get_api_key()

def get_answer_from_perplexity(message):
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {API_KEY}"
    }
    
    payload = {
        "model": "llama-3-sonar-large-32k-chat", # llama-3-sonar-large-32k-online
        "messages": [
            {
                "role": "system",
                "content": "Be precise and concise."
            },
            {
                "role": "user",
                "content": message
            }
        ]
    }
    
    response = requests.post(API_ENDPOINT, headers=headers, json=payload)
    
    if response.status_code == 200:
        response_json = response.json()
        if 'choices' in response_json and len(response_json['choices']) > 0:
            answer = response_json['choices'][0]['message']['content']
            return answer
        else:
            return "Error: No answer found in the response."
    else:
        return f"Error: {response.status_code} - {response.text}"

def format_markdown_to_html(markdown_text):
    return markdown.markdown(markdown_text, extensions=['fenced_code', 'codehilite'])

class PerplexityApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Perplexity AI Chat')
        self.setGeometry(100, 100, 800, 600)  # Set the width (w) and height (h) of the window
        
        self.layout = QVBoxLayout()
        
        self.prompt_input = QTextEdit(self)
        self.prompt_input.setPlaceholderText("Enter your message here...")
        
        self.submit_button = QPushButton('Submit', self)
        self.submit_button.clicked.connect(self.handleSubmit)
        
        self.output_label = QLabel('Output:', self)
        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)
        
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidget(self.output_text)
        self.scroll_area.setWidgetResizable(True)
        
        self.layout.addWidget(self.prompt_input)
        self.layout.addWidget(self.submit_button)
        self.layout.addWidget(self.output_label)
        self.layout.addWidget(self.scroll_area)
        
        self.setLayout(self.layout)
        
    def handleSubmit(self):
        prompt = self.prompt_input.toPlainText()
        if prompt:
            answer = get_answer_from_perplexity(prompt)
            formatted_answer = format_markdown_to_html(answer)
            self.output_text.setHtml(formatted_answer)
        else:
            self.output_text.setPlainText("Please enter a message.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = PerplexityApp()
    ex.show()
    sys.exit(app.exec())
