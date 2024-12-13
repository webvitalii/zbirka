import dns.resolver
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                               QPushButton, QTextEdit, QProgressBar)
from PySide6.QtCore import QThread, Signal
import socket
import ssl
import requests
from urllib.parse import urlparse
import re

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
            self.update_progress.emit(20)
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
            self.update_progress.emit(40)
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

            # HTTP Headers and Content
            self.update_progress.emit(60)
            self.update_result.emit("\nFetching HTTP Headers and Content...\n")
            try:
                response = requests.get(self.url, allow_redirects=True, timeout=10)
                
                # Headers
                self.update_result.emit("HTTP Headers:\n")
                for header, value in response.headers.items():
                    self.update_result.emit(f"{header}: {value}\n")
                
                # Status Code
                self.update_result.emit(f"\nStatus Code: {response.status_code}\n")
                
                # Content Type
                self.update_result.emit(f"Content Type: {response.headers.get('Content-Type', 'Not specified')}\n")
                
                # Page Size
                self.update_result.emit(f"Page Size: {len(response.content)} bytes\n")
                
                # Extract information from content
                content = response.text
                
                # Title (using regex)
                title_match = re.search('<title>(.*?)</title>', content, re.IGNORECASE)
                title = title_match.group(1) if title_match else "No title found"
                self.update_result.emit(f"Page Title: {title}\n")
                
                # Meta description (using regex)
                meta_desc_match = re.search('<meta\\s+name=["\']description["\']\\s+content=["\'](.*?)["\']', content, re.IGNORECASE)
                if meta_desc_match:
                    self.update_result.emit(f"Meta Description: {meta_desc_match.group(1)}\n")
                
                # Links count
                links_count = content.count('<a ')
                self.update_result.emit(f"Number of links: {links_count}\n")
                
                # Images count
                images_count = content.count('<img ')
                self.update_result.emit(f"Number of images: {images_count}\n")
                
                # Scripts count
                scripts_count = content.count('<script')
                self.update_result.emit(f"Number of scripts: {scripts_count}\n")
                
                # Stylesheets count
                stylesheets_count = len(re.findall('<link[^>]+rel=["\'](stylesheet|style)["\']', content, re.IGNORECASE))
                self.update_result.emit(f"Number of stylesheets: {stylesheets_count}\n")
                
            except requests.RequestException as e:
                self.update_result.emit(f"Error fetching HTTP content: {str(e)}\n")

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