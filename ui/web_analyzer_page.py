import dns.resolver
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                               QPushButton, QTextEdit, QProgressBar)
from PySide6.QtCore import QThread, Signal
import socket
import ssl
import requests
from urllib.parse import urlparse

class WebAnalyzerThread(QThread):
    update_progress = Signal(int)
    update_result = Signal(str)
    analysis_complete = Signal()

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        try:
            self.update_progress.emit(10)
            self.update_result.emit("Starting analysis...\n")

            # Normalize URL
            if not self.url.startswith('http'):
                self.url = 'http://' + self.url
            parsed_url = urlparse(self.url)
            domain = parsed_url.netloc

            # DNS information
            self.update_progress.emit(30)
            self.update_result.emit("\nFetching DNS information...\n")
            for qtype in ['A', 'AAAA', 'MX', 'NS', 'TXT']:
                try:
                    answers = dns.resolver.resolve(domain, qtype)
                    for rdata in answers:
                        self.update_result.emit(f"{qtype} Record: {rdata}\n")
                except dns.resolver.NoAnswer:
                    self.update_result.emit(f"No {qtype} record found\n")
                except Exception as e:
                    self.update_result.emit(f"Error fetching {qtype} record: {str(e)}\n")

            # SSL Certificate information
            self.update_progress.emit(60)
            self.update_result.emit("\nChecking SSL Certificate...\n")
            try:
                context = ssl.create_default_context()
                with socket.create_connection((domain, 443)) as sock:
                    with context.wrap_socket(sock, server_hostname=domain) as secure_sock:
                        cert = secure_sock.getpeercert()
                        subject = dict(x[0] for x in cert['subject'])
                        issuer = dict(x[0] for x in cert['issuer'])
                        self.update_result.emit(f"Subject: {subject.get('commonName')}\n")
                        self.update_result.emit(f"Issuer: {issuer.get('commonName')}\n")
                        self.update_result.emit(f"Version: {cert.get('version')}\n")
                        self.update_result.emit(f"Serial Number: {cert.get('serialNumber')}\n")
                        self.update_result.emit(f"Not Before: {cert.get('notBefore')}\n")
                        self.update_result.emit(f"Not After: {cert.get('notAfter')}\n")
            except Exception as e:
                self.update_result.emit(f"SSL Certificate Error: {str(e)}\n")

            # HTTP Headers
            self.update_progress.emit(80)
            self.update_result.emit("\nFetching HTTP Headers...\n")
            try:
                response = requests.head(self.url, allow_redirects=True)
                for header, value in response.headers.items():
                    self.update_result.emit(f"{header}: {value}\n")
            except requests.RequestException as e:
                self.update_result.emit(f"Error fetching HTTP headers: {str(e)}\n")

            self.update_progress.emit(100)
            self.update_result.emit("\nAnalysis complete!\n")
        except Exception as e:
            self.update_result.emit(f"An error occurred: {str(e)}\n")
        finally:
            self.analysis_complete.emit()

class WebAnalyzerPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # URL input
        url_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter website URL")
        self.analyze_button = QPushButton("Analyze")
        self.analyze_button.clicked.connect(self.start_analysis)
        url_layout.addWidget(self.url_input)
        url_layout.addWidget(self.analyze_button)
        layout.addLayout(url_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        # Results area
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        layout.addWidget(self.results_text)

        self.setLayout(layout)

    def start_analysis(self):
        url = self.url_input.text().strip()
        if not url:
            self.results_text.setText("Please enter a valid URL")
            return

        self.results_text.clear()
        self.progress_bar.setValue(0)
        self.analyze_button.setEnabled(False)

        self.analyzer_thread = WebAnalyzerThread(url)
        self.analyzer_thread.update_progress.connect(self.update_progress)
        self.analyzer_thread.update_result.connect(self.update_result)
        self.analyzer_thread.analysis_complete.connect(self.analysis_complete)
        self.analyzer_thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def update_result(self, result):
        self.results_text.append(result)

    def analysis_complete(self):
        self.analyze_button.setEnabled(True)