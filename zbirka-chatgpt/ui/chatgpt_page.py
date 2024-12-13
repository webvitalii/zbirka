from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                                  QTextEdit, QPushButton, QLabel)
from PySide6.QtCore import Qt
from openai import OpenAI
import os
import httpx
from pathlib import Path
import json

class ChatGPTPage(QWidget):
    def __init__(self):
        super().__init__()
        self.client = None
        self.chat_history = []
        self.setup_ui()
        self.load_api_key()
        
    def load_api_key(self):
        try:
            settings_file = Path(os.path.dirname(os.path.dirname(__file__))) / 'settings.json'
            if settings_file.exists():
                with open(settings_file, 'r') as f:
                    settings = json.load(f)
                    api_key = settings.get('api_key', '')
                    if api_key:
                        self.update_api_key(api_key)
        except Exception:
            pass
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Status label
        self.status_label = QLabel()
        self.status_label.setStyleSheet("color: red;")
        layout.addWidget(self.status_label)
        
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
        if key:
            try:
                self.client = OpenAI(api_key=key)
                self.status_label.setText("")
                self.status_label.setStyleSheet("color: green;")
                
                # Test the API key
                self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": "test"}],
                    max_tokens=5
                )
            except Exception as e:
                self.client = None
                self.status_label.setText("")
                self.status_label.setStyleSheet("color: red;")
                self.chat_display.append(f"Error validating API key: {str(e)}\n")
        else:
            self.client = None
            self.status_label.setText("API Key Not Set")
            self.status_label.setStyleSheet("color: red;")
        
    def send_message(self):
        if not self.client:
            self.chat_display.append("Please set your OpenAI API key in Settings first.\n")
            return
            
        user_message = self.user_input.toPlainText().strip()
        if not user_message:
            return
            
        # Add user message to chat history
        self.chat_history.append({"role": "user", "content": user_message})
        self.chat_display.append(f"You: {user_message}\n")
        
        try:
            # Get response from ChatGPT
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=self.chat_history
            )
            
            # Extract and display the response
            assistant_message = response.choices[0].message.content
            self.chat_history.append({"role": "assistant", "content": assistant_message})
            self.chat_display.append(f"Assistant: {assistant_message}\n")
            
        except httpx.ConnectError:
            error_msg = ("Connection error: Unable to connect to OpenAI servers.\n"
                        "This might be due to:\n"
                        "1. No internet connection\n"
                        "2. Firewall blocking the connection\n"
                        "3. Need for proxy configuration")
            self.chat_display.append(f"Error: {error_msg}\n")
        except httpx.TimeoutException:
            self.chat_display.append("Error: Request timed out. Please try again.\n")
        except Exception as e:
            self.chat_display.append(f"Error: {str(e)}\n")
            
        # Clear input field
        self.user_input.clear()
