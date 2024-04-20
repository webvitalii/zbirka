from PySide6.QtWidgets import QWidget, QLineEdit, QTextEdit, QPushButton, QVBoxLayout
from PySide6.QtCore import QUrl
import dns.resolver
import whois

class WhoisPage(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Enter URL")
        self.layout.addWidget(self.text_input)

        self.whois_btn = QPushButton("Whois Lookup")
        self.whois_btn.clicked.connect(self.get_whois_info)
        self.layout.addWidget(self.whois_btn)
        
        self.dns_btn = QPushButton("DNS Lookup")
        self.dns_btn.clicked.connect(self.get_dns_info)
        self.layout.addWidget(self.dns_btn)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)  # Make output text non-editable
        self.layout.addWidget(self.output_text)

        self.setLayout(self.layout)
        
        
    def get_whois_info(self):
        url = self.text_input.text()

        # Validate URL format
        if not QUrl(url).isValid():
            self.output_text.setText("Invalid URL format. Please enter a valid URL.")
            return

        # Extract domain name from URL
        domain_name = QUrl(url).host()
        
        try:
            whois_info = whois.whois(domain_name)
            self.output_text.setText(str(whois_info))
        except Exception as e:
            self.output_text.setText("Invalid URL format. Please enter a valid URL.") # str(e)
            
    def get_whois_info_old(self):
        url = self.text_input.text()

        # Validate URL format
        if not QUrl(url).isValid():
            self.output_text.setText("Invalid URL format. Please enter a valid URL.")
            return

        # Extract domain name from URL
        domain_name = QUrl(url).host()

        try:
            whois_data = whois.query(domain_name)
            self.output_text.setText(str(whois_data))
        except whois.Exception as e:
            self.output_text.setText(f"Error: {str(e)}")

            
    def get_dns_info(self):
        url = self.text_input.text()

        # Validate URL format
        if not QUrl(url).isValid():
            self.output_text.setText("Invalid URL format. Please enter a valid URL.")
            return

        # Extract domain name from URL
        domain_name = QUrl(url).host()

        try:
            resolver = dns.resolver.Resolver()
            w = resolver.whois(domain_name)
            whois_info = str(w)
            self.output_text.setText(whois_info)
        except dns.resolver.NXDOMAIN:
            self.output_text.setText(f"Domain '{domain_name}' not found.")
        except dns.resolver.ResolverError as e:
            self.output_text.setText(f"Error: {str(e)}")