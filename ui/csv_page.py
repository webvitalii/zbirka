from PySide6.QtWidgets import (QWidget, QLineEdit, QTextEdit, QPushButton, 
                               QVBoxLayout, QHBoxLayout, QFileDialog, QLabel, 
                               QMessageBox, QProgressBar)
from PySide6.QtCore import QThread, Signal
import csv

class CsvConverterThread(QThread):
    progress_update = Signal(int)
    conversion_complete = Signal(str)
    error_occurred = Signal(str)

    def __init__(self, input_file, output_file, selected_fields, input_delimiter, output_delimiter):
        super().__init__()
        self.input_file = input_file
        self.output_file = output_file
        self.selected_fields = selected_fields
        self.input_delimiter = input_delimiter
        self.output_delimiter = output_delimiter

    def run(self):
        try:
            with open(self.input_file, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=self.input_delimiter)
                fieldnames = reader.fieldnames
                
                # Filter and order fields based on user selection
                filtered_fieldnames = [field.strip() for field in self.selected_fields if field.strip() in fieldnames]
                
                total_rows = sum(1 for row in csvfile)
                csvfile.seek(0)
                next(reader)  # Skip header row
                
                with open(self.output_file, 'w', newline='', encoding='utf-8') as new_csvfile:
                    writer = csv.DictWriter(new_csvfile, fieldnames=filtered_fieldnames, delimiter=self.output_delimiter)
                    writer.writeheader()
                    
                    for i, row in enumerate(reader, 1):
                        filtered_row = {key: row[key] for key in filtered_fieldnames}
                        writer.writerow(filtered_row)
                        self.progress_update.emit(int(i / total_rows * 100))
                
                self.conversion_complete.emit(self.output_file)
        except Exception as e:
            self.error_occurred.emit(str(e))

class CsvPage(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_file_path = None
        self.current_delimiter = ","
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        # File selection
        file_layout = QHBoxLayout()
        self.csv_file_path_input = QLineEdit()
        self.select_csv_file_btn = QPushButton("Browse to select a CSV file")
        self.select_csv_file_btn.clicked.connect(self.select_csv_file)
        file_layout.addWidget(self.csv_file_path_input)
        file_layout.addWidget(self.select_csv_file_btn)
        self.layout.addLayout(file_layout)

        # Fields selection
        self.csv_fields_label = QLabel("Enter CSV fields to export (comma-separated, order matters)")
        self.layout.addWidget(self.csv_fields_label)
        self.csv_fields_input = QLineEdit()
        self.layout.addWidget(self.csv_fields_input)

        # Current delimiter display
        self.current_delimiter_label = QLabel(f"Current delimiter: {self.current_delimiter}")
        self.layout.addWidget(self.current_delimiter_label)

        # New delimiter input
        new_delimiter_layout = QHBoxLayout()
        self.new_delimiter_label = QLabel("New delimiter:")
        self.new_delimiter_input = QLineEdit(self.current_delimiter)
        self.new_delimiter_input.setMaximumWidth(30)
        new_delimiter_layout.addWidget(self.new_delimiter_label)
        new_delimiter_layout.addWidget(self.new_delimiter_input)
        new_delimiter_layout.addStretch()
        self.layout.addLayout(new_delimiter_layout)

        # Convert button
        self.create_csv_file_btn = QPushButton("Convert CSV")
        self.create_csv_file_btn.clicked.connect(self.create_new_csv_file)
        self.layout.addWidget(self.create_csv_file_btn)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.layout.addWidget(self.progress_bar)

        # Output text
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.layout.addWidget(self.output_text)

        self.setLayout(self.layout)

    def select_csv_file(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("CSV files (*.csv)")
        if file_dialog.exec_():
            file_paths = file_dialog.selectedFiles()
            if file_paths:
                self.selected_file_path = file_paths[0]
                self.csv_file_path_input.setText(self.selected_file_path)
                self.load_csv_fields()
                self.output_text.clear()

    def load_csv_fields(self):
        try:
            with open(self.selected_file_path, 'r', newline='', encoding='utf-8') as csvfile:
                dialect = csv.Sniffer().sniff(csvfile.read(1024))
                csvfile.seek(0)
                self.current_delimiter = dialect.delimiter
                self.current_delimiter_label.setText(f"Current delimiter: {self.current_delimiter}")
                self.new_delimiter_input.setText(self.current_delimiter)
                
                reader = csv.reader(csvfile, delimiter=self.current_delimiter)
                fields = next(reader)
                self.csv_fields_input.setText(','.join(fields))
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load CSV fields: {str(e)}")

    def create_new_csv_file(self):
        if not self.selected_file_path:
            QMessageBox.warning(self, "Error", "Please select a CSV file first.")
            return

        selected_fields = [field.strip() for field in self.csv_fields_input.text().split(',')]
        if not selected_fields:
            QMessageBox.warning(self, "Error", "Please enter at least one field to export.")
            return

        output_file, _ = QFileDialog.getSaveFileName(self, "Save Converted CSV", "", "CSV Files (*.csv)")
        if not output_file:
            return

        self.progress_bar.setVisible(True)
        self.create_csv_file_btn.setEnabled(False)
        self.output_text.clear()

        self.converter_thread = CsvConverterThread(
            self.selected_file_path, output_file, selected_fields, 
            self.current_delimiter, self.new_delimiter_input.text())
        self.converter_thread.progress_update.connect(self.update_progress)
        self.converter_thread.conversion_complete.connect(self.conversion_completed)
        self.converter_thread.error_occurred.connect(self.conversion_error)
        self.converter_thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def conversion_completed(self, output_file):
        self.progress_bar.setVisible(False)
        self.create_csv_file_btn.setEnabled(True)
        self.output_text.append(f"Conversion completed successfully. Output file: {output_file}")

    def conversion_error(self, error_message):
        self.progress_bar.setVisible(False)
        self.create_csv_file_btn.setEnabled(True)
        QMessageBox.critical(self, "Error", f"An error occurred during conversion: {error_message}")
        self.output_text.append(f"Error: {error_message}")