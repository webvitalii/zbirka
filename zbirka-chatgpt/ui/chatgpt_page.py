from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                                  QTextEdit, QPushButton, QLabel, QLineEdit)
from PySide6.QtCore import Qt
from openai import OpenAI

class ChatGPTPage(QWidget):
    def __init__(self):
        super().__init__()
        self.api_key = None
        self.client = None
        self.chat_history = []
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # API Key section
        api_key_layout = QHBoxLayout()
        api_key_label = QLabel("API Key:")
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.Password)
        self.api_key_input.textChanged.connect(self.update_api_key)
        api_key_layout.addWidget(api_key_label)
        api_key_layout.addWidget(self.api_key_input)
        layout.addLayout(api_key_layout)
        
        # Chat history display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setMinimumHeight(300)
        layout.addWidget(self.chat_display)
        
        # User input area
        self.user_input = QTextEdit()
        self.user_input.setMaximumHeight(100)
        self.user_input.setPlaceholderText("Type your message here...")
        layout.addWidget(self.user_input)
        
        # Send button
        send_layout = QHBoxLayout()
        send_layout.addStretch()
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        send_layout.addWidget(self.send_button)
        layout.addLayout(send_layout)
        
        self.setLayout(layout)
        
    def update_api_key(self, key):
        self.api_key = key
        self.client = OpenAI(api_key=key)
        
    def send_message(self):
        if not self.api_key or not self.client:
            self.chat_display.append("Please enter your OpenAI API key first.")
            return
            
        user_message = self.user_input.toPlainText().strip()
        if not user_message:
            return
            
        # Add user message to chat history
        self.chat_history.append({"role": "user", "content": user_message})
        self.chat_display.append(f"You: {user_message}\n")
        
        try:
            # Get response from ChatGPT using the new API format
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=self.chat_history
            )
            
            # Extract and display the response
            assistant_message = response.choices[0].message.content
            self.chat_history.append({"role": "assistant", "content": assistant_message})
            self.chat_display.append(f"Assistant: {assistant_message}\n")
            
        except Exception as e:
            self.chat_display.append(f"Error: {str(e)}\n")
            
        # Clear input field
        self.user_input.clear()
